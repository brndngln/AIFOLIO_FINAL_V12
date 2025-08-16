#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const EXCLUDED = new Set([
  '.git', '.venv', 'venv', 'node_modules', 'dist', 'build', 'coverage',
  '.pytest_cache', '.mypy_cache', '.ruff_cache', '.cache', '.next', '.turbo', '.windsurf', '.DS_Store'
]);

function isExcluded(p) {
  return p.split(path.sep).some(part => EXCLUDED.has(part));
}

function* walk(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (isExcluded(full)) continue;
    if (e.isDirectory()) {
      yield* walk(full);
    } else {
      yield full;
    }
  }
}

function rel(p) {
  return p.split(path.sep).join('/');
}

function readJSONSafe(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    return null;
  }
}

function parseTsConfig(root) {
  const tsconfigPath = path.join(root, 'tsconfig.json');
  const data = readJSONSafe(tsconfigPath);
  if (!data) return { baseUrl: '.', paths: {} };
  const compilerOptions = data.compilerOptions || {};
  return { baseUrl: compilerOptions.baseUrl || '.', paths: compilerOptions.paths || {} };
}

function extractImports(code) {
  const imports = [];
  // Very naive, non-heredoc regex that handles common cases
  const re = /import\s+(?:[^'"\n]+?from\s+)?["']([^"']+)["']|require\(\s*["']([^"']+)["']\s*\)/g;
  let m;
  while ((m = re.exec(code)) !== null) {
    const spec = m[1] || m[2];
    if (spec) imports.push(spec);
  }
  return imports;
}

function main() {
  const root = process.cwd();
  const tsconfig = parseTsConfig(root);

  const exts = new Set(['.ts', '.tsx', '.js', '.jsx', '.mts', '.cts']);
  const files = [];
  for (const f of walk(root)) {
    const ext = path.extname(f).toLowerCase();
    if (!exts.has(ext)) continue;
    files.push(f);
  }

  const edges = {};
  for (const f of files) {
    let code = '';
    try { code = fs.readFileSync(f, 'utf8'); } catch {}
    const imps = extractImports(code).map(s => ({ module: s }));
    edges[rel(path.relative(root, f))] = imps;
  }

  const out = {
    tsconfig,
    counts: { files: Object.keys(edges).length, imports: Object.values(edges).reduce((a, v) => a + v.length, 0) },
    edges,
  };

  const outDir = path.join(root, '.windsurf', 'fixrunner');
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'ts_graph.json'), JSON.stringify(out, null, 2));

  // Update report.json
  let report = {};
  try { report = JSON.parse(fs.readFileSync(path.join(outDir, 'report.json'), 'utf8')); } catch {}
  report.typescript = report.typescript || {};
  report.typescript.graph = { path: '.windsurf/fixrunner/ts_graph.json', counts: out.counts };
  fs.writeFileSync(path.join(outDir, 'report.json'), JSON.stringify(report, null, 2));

  // checkpoint
  const checkpoints = fs.readdirSync(outDir).filter(n => /^checkpoint_\d+\.json$/.test(n)).sort();
  const idx = checkpoints.length ? (parseInt(checkpoints[checkpoints.length - 1].match(/(\d+)/)[1], 10) + 1) : 1;
  fs.writeFileSync(path.join(outDir, `checkpoint_${idx}.json`), JSON.stringify({ step: 'ts_graph', counts: out.counts }, null, 2));

  process.stdout.write(`TS graph built for ${out.counts.files} files.\n`);
}

if (require.main === module) {
  main();
}
