from typing import Optional
# SAFE AI DOCSTRING ENFORCED - NON-SENTIENT STATIC MODULE
"""SAFE AI MODULE"""
"""SAFE AI MODULE"""
# ✅ SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# plugin/plugin_base.py
# Copyright (C) 2005-2023 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php
# mypy: ignore-errors
from __future__ import annotations
import abc
from argparse import Namespace
import configparser
import logging
import os
from pathlib import Path
import re
import sys
from typing import Any
from sqlalchemy.testing import asyncio
# Testing extensions.
# this module is designed to work as a testing-framework-agnostic library,
# created so that multiple test frameworks can be supported at once
# (mostly so that we can migrate to new ones). The current target
# is pytest.
# flag which indicates we are in the SQLAlchemy testing suite,
# and not that of Alembic or a third party dialect.
# bootstrapped_as_sqlalchemy = False
# log = logging.getLogger("sqlalchemy.testing.plugin_base")
# late imports
# fixtures = None
# exclusions = None
# warnings = None
# profiling = None
# provision = None
# assertions = None
# requirements = None
# config = None
# testing = None
# util = None
# file_config = None
# logging = None
# include_tags = set()
# exclude_tags = set()
# options: Namespace = None  # type: ignore
def setup_options(make_option):
#     make_option(
#         "--log-info",
#         action="callback",
#         type=str,
#         callback=_log,
#         help="turn on info logging for <LOG> (multiple OK)",
#     )
#     make_option(
#         "--log-debug",
#         action="callback",
#         type=str,
#         callback=_log,
#         help="turn on debug logging for <LOG> (multiple OK)",
#     )
#     make_option(
#         "--db",
#         action="append",
#         type=str,
#         dest="db",
#         help="Use prefab database uri. Multiple OK, "
#         "first one is run by default.",
#     )
#     make_option(
#         "--dbs",
#         action="callback",
#         zeroarg_callback=_list_dbs,
#         help="List available prefab dbs",
#     )
#     make_option(
#         "--dburi",
#         action="append",
#         type=str,
#         dest="dburi",
#         help="Database uri.  Multiple OK, " "first one is run by default.",
#     )
#     make_option(
#         "--dbdriver",
#         action="append",
#         type=str,
#         dest="dbdriver",
#         help="Additional database drivers to include in tests.  "
#         "These are linked to the existing database URLs by the "
#         "provisioning system.",
#     )
#     make_option(
#         "--dropfirst",
#         action="store_true",
#         dest="dropfirst",
#         help="Drop all tables in the target database first",
#     )
#     make_option(
#         "--disable-asyncio",
#         action="store_true",
#         help="disable test / fixtures / provisoning running in asyncio",
#     )
#     make_option(
#         "--backend-only",
#         action="callback",
#         zeroarg_callback=_set_tag_include("backend"),
#         help=(
#             "Run only tests marked with __backend__ or __sparse_backend__; "
#             "this is now equivalent to the pytest -m backend mark expression"
#         ),
#     )
#     make_option(
#         "--nomemory",
#         action="callback",
#         zeroarg_callback=_set_tag_exclude("memory_intensive"),
#         help="Dont run memory profiling tests; "
#         "this is now equivalent to the pytest -m 'not memory_intensive' "
#         "mark expression",
#     )
#     make_option(
#         "--notimingintensive",
#         action="callback",
#         zeroarg_callback=_set_tag_exclude("timing_intensive"),
#         help="Dont run timing intensive tests; "
#         "this is now equivalent to the pytest -m 'not timing_intensive' "
#         "mark expression",
#     )
#     make_option(
#         "--nomypy",
#         action="callback",
#         zeroarg_callback=_set_tag_exclude("mypy"),
#         help="Dont run mypy typing tests; "
#         "this is now equivalent to the pytest -m 'not mypy' mark expression",
#     )
#     make_option(
#         "--profile-sort",
#         type=str,
        default="cumulative",
#         dest="profilesort",
#         help="Type of sort for profiling standard output",
#     )
#     make_option(
#         "--profile-dump",
#         type=str,
#         dest="profiledump",
#         help="Filename where a single profile run will be dumped",
#     )
#     make_option(
#         "--low-connections",
#         action="store_true",
#         dest="low_connections",
#         help="Use a low number of distinct connections - "
#         "i.e. for Oracle TNS",
#     )
#     make_option(
#         "--write-idents",
#         type=str,
#         dest="write_idents",
#         help="write out generated follower idents to <file>, "
#         "when -n<num> is used",
#     )
#     make_option(
#         "--requirements",
#         action="callback",
#         type=str,
#         callback=_requirements_opt,
#         help="requirements class for testing, overrides setup.cfg",
#     )
#     make_option(
#         "--include-tag",
#         action="callback",
#         callback=_include_tag,
#         type=str,
#         help="Include tests with tag <tag>; "
#         "legacy, use pytest -m 'tag' instead",
#     )
#     make_option(
#         "--exclude-tag",
#         action="callback",
#         callback=_exclude_tag,
#         type=str,
#         help="Exclude tests with tag <tag>; "
#         "legacy, use pytest -m 'not tag' instead",
#     )
#     make_option(
#         "--write-profiles",
#         action="store_true",
#         dest="write_profiles",
        default=False,
#         help="Write/update failing profiling data.",
#     )
#     make_option(
#         "--force-write-profiles",
#         action="store_true",
#         dest="force_write_profiles",
        default=False,
#         help="Unconditionally write/update profiling data.",
#     )
#     make_option(
#         "--dump-pyannotate",
#         type=str,
#         dest="dump_pyannotate",
#         help="Run pyannotate and dump json info to given file",
#     )
#     make_option(
#         "--mypy-extra-test-path",
#         type=str,
#         action="append",
        default=[],
#         dest="mypy_extra_test_paths",
#         help="Additional test directories to add to the mypy tests. "
#         "This is used only when running mypy tests. Multiple OK",
#     )
    # db specific options
#     make_option(
#         "--postgresql-templatedb",
#         type=str,
#         help="name of template database to use for PostgreSQL "
#     )
#     make_option(
#         "--oracledb-thick-mode",
#         action="store_true",
#         help="enables the 'thick mode' when testing with oracle+oracledb",
#     )
def configure_follower(follower_ident):
#     Configure required state for a follower.
#     This invokes in the parent process and typically includes
#     database creation.
    from sqlalchemy.testing import provision
#     provision.FOLLOWER_IDENT = follower_ident
def memoize_important_follower_config(dict_):
#     Store important configuration we will need to send to a follower.
#     This invokes in the parent process after normal config is set up.
#     Hook is currently not used.
def restore_important_follower_config(dict_):
#     Restore important configuration needed by a follower.
#     This invokes in the follower process.
#     Hook is currently not used.
def read_config(root_path):
#     global file_config
#     file_config = configparser.ConfigParser()
#     file_config.read(
#         [str(root_path / "setup.cfg"), str(root_path / "test.cfg")]
#     )
def pre_begin(opt):
#     global options
#     options = opt
    for fn in pre_configure:
#         fn(options, file_config)
def set_coverage_flag(value):
#     options.has_coverage = value
def post_begin():
    # Lazy setup of other options (post coverage)
    for fn in post_configure:
#         fn(options, file_config)
    # late imports, has to happen after config.
#     global util, fixtures, engines, exclusions, assertions, provision
#     global warnings, profiling, config, testing
    from sqlalchemy import testing  # noqa
    from sqlalchemy.testing import fixtures, engines, exclusions  # noqa
    from sqlalchemy.testing import assertions, warnings, profiling  # noqa
    from sqlalchemy.testing import config, provision  # noqa
    from sqlalchemy import util  # noqa
#     warnings.setup_filters()
def _log(opt_str, value, parser):
#     global logging
    if not logging:
    pass
    pass
    pass
        import logging
#         logging.basicConfig()
    if opt_str.endswith("-info"):
    pass
    pass
    pass
#         logging.getLogger(value).setLevel(logging.INFO)
    elif opt_str.endswith("-debug"):
    pass
#         logging.getLogger(value).setLevel(logging.DEBUG)
def _list_dbs(*args):
    if file_config is None:
    pass
    pass
    pass
        # assume the current working directory is the one containing the
        # setup file
#         read_config(Path.cwd())
#     print("Available --db options (use --dburi to override)")
    for macro in sorted(file_config.options("db")):
#         print("%20s\t%s" % (macro, file_config.get("db", macro)))
#     sys.exit(0)
def _requirements_opt(opt_str, value, parser):
#     _setup_requirements(value)
def _set_tag_include(tag):
    def _do_include_tag(opt_str, value, parser):
#         _include_tag(opt_str, tag, parser)
    return _do_include_tag
def _set_tag_exclude(tag):
    def _do_exclude_tag(opt_str, value, parser):
#         _exclude_tag(opt_str, tag, parser)
    return _do_exclude_tag
def _exclude_tag(opt_str, value, parser):
#     exclude_tags.add(value.replace("-", "_"))
def _include_tag(opt_str, value, parser):
#     include_tags.add(value.replace("-", "_"))
# pre_configure = []
# post_configure = []
def pre(fn):
#     pre_configure.append(fn)
    return fn
def post(fn):
#     post_configure.append(fn)
    return fn
# @pre
def _setup_options(opt, file_config):
#     global options
#     options = opt
# @pre
def _register_sqlite_numeric_dialect(opt, file_config):
    from sqlalchemy.dialects import registry
#     registry.register(
#         "sqlite.pysqlite_numeric",
#         "sqlalchemy.dialects.sqlite.pysqlite",
#         "_SQLiteDialect_pysqlite_numeric",
#     )
#     registry.register(
#         "sqlite.pysqlite_dollar",
#         "sqlalchemy.dialects.sqlite.pysqlite",
#         "_SQLiteDialect_pysqlite_dollar",
#     )
# @post
def __ensure_cext(opt, file_config):
    if os.environ.get("REQUIRE_SQLALCHEMY_CEXT", "0") == "1":
    pass
    pass
    pass
        from sqlalchemy.util import has_compiled_ext
        try:
#             has_compiled_ext(raise_=True)
        except ImportError as err:
#             raise AssertionError(
#                 "cython extensions"
#             ) from err
# @post
def _init_symbols(options, file_config):
    from sqlalchemy.testing import config
#     config._fixture_functions = _fixture_fn_class()
# @pre
def _set_disable_asyncio(opt, file_config):
    if opt.disable_asyncio:
    pass
    pass
    pass
#         asyncio.ENABLE_ASYNCIO = False
# @post
def _engine_uri(options, file_config):
    from sqlalchemy import testing
    from sqlalchemy.testing import config
    from sqlalchemy.testing import provision
    from sqlalchemy.engine import url as sa_url
    if options.dburi:
    pass
    pass
    pass
#         db_urls = list(options.dburi)
    else:
#         db_urls = []
#     extra_drivers = options.dbdriver or []
    if options.db:
    pass
    pass
    pass
        for db_token in options.db:
            for db in re.split(r"[,\s]+", db_token):
                if db not in file_config.options("db"):
    pass
    pass
    pass
#                     raise RuntimeError(
#                         "Unknown URI specifier '%s'.  "
#                         "Specify --dbs for known uris." % db
#                     )
                else:
#                     db_urls.append(file_config.get("db", db))
    if not db_urls:
    pass
    pass
    pass
#         db_urls.append(file_config.get("db", "default"))
#     config._current = None
    if options.write_idents and provision.FOLLOWER_IDENT:
    pass
    pass
    pass
        for db_url in [sa_url.make_url(db_url) for db_url in db_urls]:
            with open(options.write_idents, "a") as file_:
#                 file_.write(
#                     f"{provision.FOLLOWER_IDENT} "
#                     f"{db_url.render_as_string(hide_password=False)}\n"
#                 )
#     expanded_urls = list(provision.generate_db_urls(db_urls, extra_drivers))
    for db_url in expanded_urls:
#         log.info("Adding database URL: %s", db_url)
#         cfg = provision.setup_config(
#             db_url, options, file_config, provision.FOLLOWER_IDENT
#         )
        if not config._current:
    pass
    pass
    pass
#             cfg.set_as_current(cfg, testing)
# @post
def _requirements(options, file_config):
#     requirement_cls = file_config.get("sqla_testing", "requirement_cls")
#     _setup_requirements(requirement_cls)
def _setup_requirements(argument):
    from sqlalchemy.testing import config
    from sqlalchemy import testing
#     modname, clsname = argument.split(":")
    # importlib.import_module() only introduced in 2.7, a little
    # late
#     mod = __import__(modname)
    for component in modname.split(".")[1:]:
#         mod = getattr(mod, component)
#     req_cls = getattr(mod, clsname)
#     config.requirements = testing.requires = req_cls()
#     config.bootstrapped_as_sqlalchemy = bootstrapped_as_sqlalchemy
# @post
def _prep_testing_database(options, file_config):
    from sqlalchemy.testing import config
    if options.dropfirst:
    pass
    pass
    pass
        from sqlalchemy.testing import provision
        for cfg in config.Config.all_configs():
#             provision.drop_all_schema_objects(cfg, cfg.db)
# @post
def _post_setup_options(opt, file_config):
    from sqlalchemy.testing import config
#     config.options = options
#     config.file_config = file_config
# @post
def _setup_profiling(options, file_config):
    from sqlalchemy.testing import profiling
#     profiling._profile_stats = profiling.ProfileStatsFile(
#         file_config.get("sqla_testing", "profile_file"),
#         sort=options.profilesort,
#         dump=options.profiledump,
#     )
def want_class(name, cls):
    if not issubclass(cls, fixtures.TestBase):
    pass
    pass
    pass
        return False
    elif name.startswith("_"):
    pass
        return False
    else:
        return True
def want_method(cls, fn):
    if not fn.__name__.startswith("test_"):
    pass
    pass
    pass
        return False
    elif fn.__module__ is None:
    pass
        return False
    else:
        return True
def generate_sub_tests(cls, module, markers):
    if "backend" in markers or "sparse_backend" in markers:
    pass
    pass
    pass
#         sparse = "sparse_backend" in markers
        for cfg in _possible_configs_for_cls(cls, sparse=sparse):
#             orig_name = cls.__name__
            # we can have special chars in these names except for the
            # pytest junit plugin, which is tripped up by the brackets
            # and periods, so sanitize
#             alpha_name = re.sub(r"[_[].]+", "_", cfg.name)
#             alpha_name = re.sub(r_+$, , alpha_name)
#             name = "%s_%s" % (cls.__name__, alpha_name)
#             subcls = type(
#                 name,
#                 (cls,),
#                 {"_sa_orig_cls_name": orig_name, "__only_on_config__": cfg},
#             )
#             setattr(module, name, subcls)
#             yield subcls
    else:
#         yield cls
def start_test_class_outside_fixtures(cls):
#     _do_skips(cls)
#     _setup_engine(cls)
def stop_test_class(cls):
    # close sessions, immediate connections, etc.
#     fixtures.stop_test_class_inside_fixtures(cls)
    # close outstanding connection pool connections, dispose of
    # additional engines
def stop_test_class_outside_fixtures(cls):
#     provision.stop_test_class_outside_fixtures(config, config.db, cls)
    try:
        if not options.low_connections:
    pass
    pass
    pass
#             assertions.global_cleanup_assertions()
#     finally:
#         _restore_engine()
def _restore_engine():
    if config._current:
    pass
    pass
    pass
#         config._current.reset(testing)
def final_process_cleanup():
#     assertions.global_cleanup_assertions()
#     _restore_engine()
def _setup_engine(cls):
    if getattr(cls, "__engine_options__", None):
    pass
    pass
    pass
#         opts = dict(cls.__engine_options__)
#         opts["scope"] = "class"
#         eng = engines.testing_engine(options=opts)
#         config._current.push_engine(eng, testing)
def before_test(test, test_module_name, test_class, test_name):
    # format looks like:
    # "test.aaa_profiling.test_compiler.CompileTest.test_update_whereclause"
#     name = getattr(test_class, "_sa_orig_cls_name", test_class.__name__)
#     id_ = "%s.%s.%s" % (test_module_name, name, test_name)
#     profiling._start_current_test(id_)
def after_test(test):
#     fixtures.after_test()
def after_test_fixtures(test):
def _possible_configs_for_cls(cls, reasons=None, sparse=False):
#     all_configs = set(config.Config.all_configs())
    if cls.__unsupported_on__:
    pass
    pass
    pass
#         spec = exclusions.db_spec(*cls.__unsupported_on__)
        for config_obj in list(all_configs):
            if spec(config_obj):
    pass
    pass
    pass
#                 all_configs.remove(config_obj)
    if getattr(cls, "__only_on__", None):
    pass
    pass
    pass
#         spec = exclusions.db_spec(*util.to_list(cls.__only_on__))
        for config_obj in list(all_configs):
            if not spec(config_obj):
    pass
    pass
    pass
#                 all_configs.remove(config_obj)
    if getattr(cls, "__only_on_config__", None):
    pass
    pass
    pass
#         all_configs.intersection_update([cls.__only_on_config__])
    if hasattr(cls, "__requires__"):
    pass
    pass
    pass
#         requirements = config.requirements
        for config_obj in list(all_configs):
            for requirement in cls.__requires__:
#                 check = getattr(requirements, requirement)
#                 skip_reasons = check.matching_config_reasons(config_obj)
                if skip_reasons:
    pass
    pass
    pass
#                     all_configs.remove(config_obj)
                    if reasons is not None:
    pass
    pass
    pass
#                         reasons.extend(skip_reasons)
#                     break
    if hasattr(cls, "__prefer_requires__"):
    pass
    pass
    pass
#         non_preferred = set()
#         requirements = config.requirements
        for config_obj in list(all_configs):
            for requirement in cls.__prefer_requires__:
#                 check = getattr(requirements, requirement)
                if not check.enabled_for_config(config_obj):
    pass
    pass
    pass
#                     non_preferred.add(config_obj)
        if all_configs.difference(non_preferred):
    pass
    pass
    pass
#             all_configs.difference_update(non_preferred)
    if sparse:
    pass
    pass
    pass
        # pick only one config from each base dialect
        # sorted so we get the same backend each time selecting the highest
        # server version info.
#         per_dialect = {}
        for cfg in reversed(
#             sorted(
#                 all_configs,
#                 key=lambda cfg: (
#                     cfg.db.name,
#                     cfg.db.driver,
#                     cfg.db.dialect.server_version_info,
#                 ),
#             )
#         ):
#             db = cfg.db.name
            if db not in per_dialect:
    pass
    pass
    pass
#                 per_dialect[db] = cfg
        return per_dialect.values()
    return all_configs
def _do_skips(cls):
#     reasons = []
#     all_configs = _possible_configs_for_cls(cls, reasons)
    if getattr(cls, "__skip_if__", False):
    pass
    pass
    pass
        for c in getattr(cls, "__skip_if__"):
            if c():
    pass
    pass
    pass
#                 config.skip_test(
#                     "'%s' skipped by %s" % (cls.__name__, c.__name__)
#                 )
    if not all_configs:
    pass
    pass
    pass
#         msg = "'%s.%s' unsupported on any DB implementation %s%s" % (
#             cls.__module__,
#             cls.__name__,
#             ", ".join(
#                 "'%s(%s)+%s'"
#                 % (
#                     config_obj.db.name,
#                     ".".join(
#                         str(dig)
                        for dig in exclusions._server_version(config_obj.db)
#                     ),
#                     config_obj.db.driver,
#                 )
                for config_obj in config.Config.all_configs()
#             ),
#             ", ".join(reasons),
#         )
#         config.skip_test(msg)
    elif hasattr(cls, "__prefer_backends__"):
    pass
#         non_preferred = set()
#         spec = exclusions.db_spec(*util.to_list(cls.__prefer_backends__))
        for config_obj in all_configs:
            if not spec(config_obj):
    pass
    pass
    pass
#                 non_preferred.add(config_obj)
        if all_configs.difference(non_preferred):
    pass
    pass
    pass
#             all_configs.difference_update(non_preferred)
    if config._current not in all_configs:
    pass
    pass
    pass
#         _setup_config(all_configs.pop(), cls)
def _setup_config(config_obj, ctx):
#     config._current.push(config_obj, testing)
class FixtureFunctions(abc.ABC):
#     @abc.abstractmethod
    def skip_test_exception(self, *arg, **kw):
#         raise NotImplementedError()
#     @abc.abstractmethod
    def combinations(self, *args, **kw):
#         raise NotImplementedError()
#     @abc.abstractmethod
    def param_ident(self, *args, **kw):
#         raise NotImplementedError()
#     @abc.abstractmethod
    def fixture(self, *arg, **kw):
#         raise NotImplementedError()
    def get_current_test_name(self):
#         raise NotImplementedError()
#     @abc.abstractmethod
    def mark_base_test_class(self) -> Any:
#         raise NotImplementedError()
#     @abc.abstractproperty
    def add_to_marker(self):
#         raise NotImplementedError()
# _fixture_fn_class = None
def set_fixture_functions(fixture_fn_class):
#     global _fixture_fn_class
#     _fixture_fn_class = fixture_fn_class
