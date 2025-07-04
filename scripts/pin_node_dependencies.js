// Script to pin all Node.js dependencies to exact versions in package.json
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
['dependencies', 'devDependencies'].forEach(depType => {
  if (pkg[depType]) {
    Object.keys(pkg[depType]).forEach(dep => {
      if (pkg[depType][dep].startsWith('^') || pkg[depType][dep].startsWith('~')) {
        pkg[depType][dep] = pkg[depType][dep].replace(/^\^|~/, '');
      }
    });
  }
});
fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
console.log('All Node dependencies pinned to exact versions.');
