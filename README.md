# membership-payments-verify
Plaintext accounting compatible tool for managing a small number of customers that you render service to on a recurring basis. They either pay their dues or are due for a swim. With the fishes.

## Grammar

```
trn = Payment for $service [$customer] $period
period = for current month | until $date
date = dd/mm/yyyy
```

Example:
```
Payment for a_service [John] for current month
```

## Usage
For now go for [dev](#dev)

## Dev

### Prerequisites
- [nix](https://nixos.org/nix/manual/#chap-installation)
- `direnv` (`nix-env -iA nixpkgs.direnv`)
- [configured direnv shell hook ](https://direnv.net/docs/hook.html)
- some form of `make` (`nix-env -iA nixpkgs.gnumake`)

Hint: if something doesn't work because of missing package please add the package to `default.nix` instead of installing it on your computer. Why solve the problem for one if you can solve the problem for all? ;)

Also: if the direnv doesn't is work properly *and* it is installed via nix-env -> make sure your profile is sourced in your shellrc (`source ~/.nix-profile/etc/profile.d/nix.sh`).

### One-time setup
```
make init
```

### Everything
```
make help
```
