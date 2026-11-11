#include <lean/lean.h>
#include <fstream>
#include <iostream>
#include <iterator>
#include <string>

extern "C" {
void lean_initialize();
lean_object * initialize_Lean(uint8_t, lean_object *);
lean_object * l_Lean_initSearchPath(lean_object *, lean_object *, lean_object *);
lean_object * l_Lean_Name_mkSimple(lean_object *);
lean_object * lean_name_mk_string(lean_object *, lean_object *);
extern lean_object * l_Lean_Options_empty;
lean_object * lean_run_frontend(lean_object *, lean_object *, lean_object *,
    lean_object *, uint32_t, lean_object *, uint8_t, lean_object *, lean_object *, lean_object *);
lean_object * lean_write_module(lean_object *, lean_object *, lean_object *);
lean_object * lean_enable_initializer_execution(lean_object *);
}

static bool checked(lean_object *r) {
  if (lean_io_result_is_error(r)) {
    lean_io_result_show_error(r);
    lean_dec(r);
    return false;
  }
  lean_dec(r);
  return true;
}

static lean_object *moduleName(const std::string &name) {
  lean_object *result = lean_box(0);
  size_t begin = 0;
  while (true) {
    size_t end = name.find('.', begin);
    result = lean_name_mk_string(result,
      lean_mk_string(name.substr(begin, end - begin).c_str()));
    if (end == std::string::npos) break;
    begin = end + 1;
  }
  return result;
}

int main(int argc, char **argv) {
  if (argc < 4 || argc > 5) {
    std::cerr << "usage: levy-lean-api SYSROOT SOURCE MODULE [OUTPUT.olean]\n";
    return 2;
  }
  std::ifstream file(argv[2]);
  if (!file) { std::cerr << "cannot open source\n"; return 2; }
  std::string source((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
  lean_initialize();
  lean_object *r = initialize_Lean(1, lean_io_mk_world());
  lean_io_mark_end_initialization();
  if (!checked(r)) return 1;
  lean_init_task_manager();
  if (!checked(lean_enable_initializer_execution(lean_io_mk_world()))) {
    lean_finalize_task_manager(); return 1;
  }
  r = l_Lean_initSearchPath(lean_mk_string(argv[1]), lean_box(0), lean_io_mk_world());
  if (!checked(r)) { lean_finalize_task_manager(); return 1; }
  lean_inc(l_Lean_Options_empty);
  r = lean_run_frontend(lean_mk_string(source.c_str()), l_Lean_Options_empty,
    lean_mk_string(argv[2]), moduleName(argv[3]),
    0, lean_box(0), 0, lean_mk_empty_array(), lean_mk_empty_array(), lean_io_mk_world());
  if (lean_io_result_is_error(r)) {
    checked(r); lean_finalize_task_manager(); return 1;
  }
  lean_object *pair = lean_io_result_get_value(r);
  bool ok = lean_unbox(lean_ctor_get(pair, 1));
  if (ok && argc == 5) {
    lean_object *env = lean_ctor_get(pair, 0);
    lean_inc(env);
    ok = checked(lean_write_module(env, lean_mk_string(argv[4]), lean_io_mk_world()));
  }
  lean_dec(r);
  lean_finalize_task_manager();
  return ok ? 0 : 1;
}
