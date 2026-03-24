{
  description = "Wikikaingáng scripts";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    supportedSystems = ["x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin"];
    forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
  in {
    apps = forAllSystems (system: let
      pkgs = nixpkgs.legacyPackages.${system};

      python = pkgs.python312.withPackages (ps:
        with ps; [
          requests
          pandas
          matplotlib
          seaborn
          beautifulsoup4
        ]);

      mkApp = name: scriptPath: let
        runner = pkgs.writeShellScriptBin name ''
          exec ${python}/bin/python ${scriptPath}
        '';
      in {
        type = "app";
        program = "${runner}/bin/${name}";
      };
    in {
      # nix run .#contagem
      contagem = mkApp "contagem" ./contagem_artigos.py;

      # nix run .#categoria
      categoria = mkApp "checagem" ./checagem_categoria.py;
    });

    # Optional: Development shell
    devShells = forAllSystems (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python312.withPackages (ps:
        with ps; [
          requests
          pandas
          matplotlib
          seaborn
          beautifulsoup4
        ]);
    in {
      default = pkgs.mkShell {packages = [python];};
    });
  };
}
