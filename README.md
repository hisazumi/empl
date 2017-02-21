# EMPL: Embedded Pattern Language in C

## A Sample

### source code
```
%define DATA {
    int dest;
    int src;
};
...
struct DATA *p;
...
%match(DATA * p) {
    case [10, 20] {
        ...
    }
    case [< 10, < 20] {
        ...
    }
    case [_, is_good(%here)] {
        ...
    }
}
```

### generated code

```
struct DATA {
    int dest;
    int src;
};
...
struct DATA *p;
...
if (p->dest == 10 && p->src == 20) {
    ...
}else if (p->dest < 10 && p->src < 20) {
    ...
}else if (is_good(p->src)) {
    ...
}
```

## Installation

EMPL requires textX and Jinja2. 

```
pip install textX
pip install Jinja2
```

## Usage

```
python emplc.py [empl file]
```

It will generate c code to stdout.

## Limitation

- emplc can read just one file. (it implies %define descriptions should be in one file)
