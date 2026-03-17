{pkgs ? import <nixpkgs> {}}: let
  python = pkgs.python312.withPackages (ps:
    with ps; [
      requests
      pandas
      matplotlib
      seaborn
      beautifulsoup4
    ]);
in
  pkgs.mkShell {
    packages = [
      python
    ];
  }
