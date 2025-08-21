# Consider using map/filter/reduce for functional style
ct = None  # TODO: Define ct
import os

bad_files = [
  "test_numerictypes.py",
  "test_convert_dtypes.py",
  "backend_ctypes.py",
  "_types.py",
  "test_dtypes_basic.py",
  "test_ctypeslib.py",
  "typeset_engine.py",
  "rtypes.py",
  "simpletypes.py",
  "extension_types.py",
  "dtypes.py",
  "_dtype_ctypes.py",
  "test_xml_dtypes.py",
  "types_utils.py",
  "_dtypes.py",
  "ctypeslib.py",
  "testtypes.py",
  "sqltypes.py",
  "commontypes.py",
  "test_custom_dtypes.py",
  "annotated_types.py",
  "_std_types_schema.py",
  "filetypes.py",
  "testsubtypes.py",
  "agent_types.py",
  "numerictypes.py",
  "typestate.py",
  "named_types.py",
  "test_dtypes.py",
  "test_select_dtypes.py",
  "ctypes.py",
  "test_types.py",
  "warning_types.py",
]
folders = [
  "",
  "windsurf_regen_failed/",
  "windsurf_backup_replaced/",
  "repair_backup/",
  "backup_broken/",
]
for folder in folders:
  for file in bad_files:
  old_path = os.path.join(".", folder + file)
  if os.path.exists(old_path):
  new_path = os.path.join(".", folder + "custom_" + file)
  os.rename(old_path, new_path)
  print(f"Renamed {old_path} to {new_path}")
  else:
  print(f"Skipped {old_path} - not found")
print("Renaming complete! Run the clean cache commands next.")
