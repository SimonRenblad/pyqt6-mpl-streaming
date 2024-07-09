{
  description = "base dev shell for pyqt development";
  inputs.nixpkgs.url = github:NixOS/nixpkgs/nixos-unstable;
  outputs = { self, nixpkgs}:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
    in {
      devShell.x86_64-linux = pkgs.mkShell {
        name = "pyqt-dev-shell";
        buildInputs = with pkgs; [
          openocd
          ] ++ (with python3Packages; [
            numpy matplotlib pyqt6
          ]);
        shellHook = ''
          export QT_QPA_PLATFORM=xcb
          export QT_PLUGIN_PATH=${pkgs.qt6.qtbase}/${pkgs.qt6.qtbase.dev.qtPluginPrefix}
          export QML2_IMPORT_PATH=${pkgs.qt6.qtbase}/${pkgs.qt6.qtbase.dev.qtQmlPrefix}
        '';
      };
    };
}

