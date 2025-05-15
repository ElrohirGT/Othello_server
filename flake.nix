{
  description = "Othello Server Flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    # System types to support.
    supportedSystems = ["x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin"];

    # Helper function to generate an attrset '{ x86_64-linux = f "x86_64-linux"; ... }'.
    forAllSystems = nixpkgs.lib.genAttrs supportedSystems;

    # Nixpkgs instantiated for supported system types.
    nixpkgsFor = forAllSystems (system: import nixpkgs {inherit system;});
    pythonPkgs = p: [
      p.fastapi
      p.fastjsonschema
      p.httptools
      p.pandas
      p.pydantic
      p.requests
      p.streamlit
      p.uvicorn
    ];
  in {
    packages = forAllSystems (system: let
      pkgs = nixpkgsFor.${system};
      python = pkgs.python3.withPackages pythonPkgs;
    in {
      default = pkgs.writeShellApplication {
        name = "othello server and frontend";
        runtimeInputs = [python pkgs.process-compose];
        text = ''
          process-compose
        '';
      };
    });
    devShells = forAllSystems (system: let
      pkgs = nixpkgsFor.${system};
      python = pkgs.python3.withPackages pythonPkgs;
    in {
      default = pkgs.mkShell {
        packages = [python pkgs.black pkgs.process-compose];
      };
    });
  };
}
