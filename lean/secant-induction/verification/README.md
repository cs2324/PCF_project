# Verification frontend

The normal Lean launcher cannot discover its installation path in this
workspace because its process-executable metadata lookup is unavailable.
No process-access restrictions were changed.

The included `lean_api_frontend.cpp` accepts the installation path
explicitly, initializes Lean's search path, and invokes the exported
official Lean frontend and module writer. It links the unmodified official
Lean 4.19.0 shared library and uses frontend trust level zero.

It does not modify the proof kernel, add axioms, or interpose filesystem
calls. This adapter was checked by accepting a valid theorem, exporting
and importing its module, and rejecting an attempted proof of `False`.

With `LEAN_ROOT` pointing to an official Lean 4.19.0 installation:

```sh
g++ -O2 -fPIC -I"$LEAN_ROOT/include" lean_api_frontend.cpp \
  -L"$LEAN_ROOT/lib/lean" -Wl,-rpath,"$LEAN_ROOT/lib/lean" \
  -lleanshared -o lean-api
```

With `LEAN_PATH` containing the project and compiled Mathlib dependencies:

```sh
./lean-api "$LEAN_ROOT" path/to/File.lean Module.Name [OUTPUT.olean]
```

The standard `lake` commands in the project README remain the normal way
to reproduce the proofs elsewhere. This adapter is included only to make
the actual checking route transparent and inspectable.
