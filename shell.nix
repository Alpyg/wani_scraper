{ pkgs ? import <nixpkgs> { } }:

with pkgs;

mkShell rec {
  nativeBuildInputs = [ ];
  buildInputs = [ poetry firefox ];
  LD_LIBRARY_PATH = lib.makeLibraryPath buildInputs;
}
