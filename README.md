# Cryptography

Coursework for CSC 512, Cryptography.

---

## About

This repository consists of the coursework for my CSC 512 Cryptography class at SDSM&T. It is split into two pieces:

* [`crypto/`](crypto)
* [`homework/`](homework)

The `homework/` folder is, unsurprisingly, my homework for the course. The `crypto/` folder is my class portfolio of cryptography-related code. It is implemented as a Python module providing a number of different logical submodules.

## Dependencies

The `crypto` library has the following dependencies:

* Python 3.6+
* `gmpy2` which has its own dependencies:
    - `libgmp3-dev`
    - `libmpc-dev`
    - `libmpfr-dev`
* `numpy`
* `concurrencytest` (optional, but recommended)
* `sympy`

The dependencies may be installed on Ubuntu as follows:

* Install `python3.6` and `pip`:
    ```shell
    # Add Python3.6 apt repository if using 16.04 LTS
    sudo add-apt-repository ppa:jonathonf/python-3.6  # (only for 16.04 LTS)
    sudo apt update
    # Install Python 3.6
    sudo apt install python3.6
    sudo apt install python3.6-dev
    sudo apt install python3.6-venv
    # Install an up-to-date version of Pip
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3.6 get-pip.py

    # Use Python 3.6 as the default Python3
    sudo ln -s /usr/bin/python3.6 /usr/local/bin/python3
    sudo ln -s /usr/local/bin/pip /usr/local/bin/pip3

    # Verify installation
    python --version
    python3 --version
    $(head -1 `which pip` | tail -c +3) --version
    $(head -1 `which pip3` | tail -c +3) --version
    ```
* Install `gmpy2`
    ```shell
    # Install dependencies for pip to compile gmpy2
    sudo apt install libgmp3-dev libmpc-dev libmpfr-dev
    # Might have to use pip3 depending on the output of $(head -1 `which pip` | tail -c +3) --version
    sudo -H pip install --upgrade gmpy2
    ```
* Install other Python dependencies:
    ```shell
    sudo -H pip install --upgrade numpy sympy concurrencytest
    ```

## Documentation

Example usage may be found in the course homework and in the unit tests. Run `pydoc3 -b` and navigate to the `crypto` link to view the `crypto` library documentation.

## Unit tests

The unit tests may be ran by any of the following:

```shell
$ python3 runtests.py
$ ./runtests.py
$ python3.6 runtests.py
```

## Example usage
Here's some examples of using the `crypto` module and submodules.

* Running the unit tests with a given number of processes
    ```python
    #!/usr/bin/env python3
    from crypto.tests import runtests
    # Requires the concurrencytest library installed. Will run in serial otherwise
    runtests(processes=8)
    ```
* Some bitwise utilities
    ```python
    #!/usr/bin/env python3
    from crypto.utilities import Bitstream, lazy_pad, bits_to_string

    # One of many forms a bytestream can take
    bytestream = b'This is a test'
    # Lazily pad the bytestream so that it's length is evenly divisible by 8
    # The pad values will be randomly chosen from the given array
    bytestream = lazy_pad(bytestream, multiple=8, pad_values=b'abcdefghijklmnopqrstuvwxyz')
    # Construct a Bitstream
    bitstream = Bitstream(bytestream)

    # Hopefully unchanged
    output = bits_to_string(bitstream)
    print(output)
    # Will be `This is a test` with two random characters appended
    ```
* Some classical ciphers
    ```python
    #!/usr/bin/env python3
    from crypto.classical import AffineCipher, LfsrCipher
    import numpy

    plaintext = 'affine'
    cipher = AffineCipher(9, 2)
    ciphertext = cipher.encrypt(plaintext)
    assert ciphertext == 'cvvwpm'

    # Values taken from HW 1 problem 6
    initial_values = numpy.array([1, 0, 1, 0, 0, 1])
    coeffs = numpy.array([1, 1, 0, 1, 1, 0])
    cipher = LfsrCipher(initial_values, coeffs)

    ciphertext = cipher.encrypt('zyxwvuts')
    ciphertext = [ord(c) for c in ciphertext]
    expected = [31, 90, 153, 215, 233, 255, 13, 164]
    assert ciphertext == expected
    ```
---

## TODO list
* Portfolio writeup
    - Algorithm explanation
    - Add code examples to class and module level docstrings
    - add more verbose docstrings
* Differential Cryptanalysis for three rounds
* Sieve of Sundaram
* Wheel Factorization
