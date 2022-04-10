let
  nixpkgs = builtins.fetchGit {
    # 2022-04-10
    url = "https://github.com/nixos/nixpkgs-channels/";
    ref = "refs/heads/nixos-unstable";
    rev = "4762fba469e2baa82f983b262e2c06ac2fdaae67";
    # obtain via `git ls-remote https://github.com/nixos/nixpkgs-channels nixos-unstable`
  };
  pkgs = import nixpkgs { config = {}; };
  pythonPkgs = python-packages: with python-packages; [
      # dev
      ptpython

      # test
      pytest

      pyyaml
    ];
  pythonCore = pkgs.python38;
  env = pkgs.buildEnv {
    name = "env";
    paths =
    with pkgs;
    [
      # dev
      git
      gnugrep
      entr

      (pythonCore.withPackages pythonPkgs)
    ];
  };
in
{
  shell = pkgs.mkShell {
    buildInputs = [ env ];
  };
}
