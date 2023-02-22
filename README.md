<!-- PROJECT SHIELDS -->
![[GPL-3.0 License](https://github.com/r3nt0n)](https://img.shields.io/badge/license-GPL%203.0-brightgreen.svg)
![[Python 3](https://github.com/r3nt0n)](http://img.shields.io/badge/python-3-blue.svg)
![[Version 0.1.1](https://github.com/r3nt0n)](http://img.shields.io/badge/version-0.1.1-orange.svg)

<div align="center">
  <h3 align="center">multicat</h3>
  <p align="center">
    Multithread reverse shell listener
  </p>
</div>


<!-- ABOUT THE PROJECT -->
<p align="center"><img src="https://github.com/r3nt0n/multicat/blob/master/img/mc.gif" /></p>  

## Use cases
Sometimes you have to spread the same payload to multiple targets and don't know how many clients will try to connect back. Multicat allow to setup a **listener capable of handling multiple connections on the same port** and **interact with each client on a separate session**. This server is client agnostic: **compatible with any reverse shell that would work with a netcat listener**.


<p align="right">(<a href="#top">back to top</a>)</p>


<!-- INSTALLATION -->
## Installation
```commandline
pip install multicat
```

<!-- USAGE EXAMPLES -->
## Usage

To start listening on the port of your choice:
```commandline
mc -p 1234
```

### Arguments

```commandline
Usage: mc [-h] [-p] [-m] [-t]

-h, --help           show this help message and exit
-p , --port          port to listen (default: 28000)
-m , --max-clients   max number of new clients to queue before establish connection (default: 5)
-t , --timeout       connections timeout (default: 10)
```

### Commands
Available commands in general menu context:
```commandline
COMMAND         DESCRIPTION
------------------------------------
HELP            List available commands
SESSIONS        List established sessions
START <id>      Interact with a client
CLOSE <id>      Close an specific connection
EXIT / QUIT     Exit the entire application
```

Available commands in session context:
````commandline
COMMAND         DESCRIPTION
------------------------------------
STOP            Stop interacting with the current session
CLOSE           Close the current connection
````

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LEGAL DISCLAIMER -->
## Legal disclaimer
This tool is created for the sole purpose of security awareness and education, it should not be used against systems that you do not have permission to test/attack. The author is not responsible for misuse or for any damage that you may cause. You agree that you use this software at your own risk.

<p align="right">(<a href="#top">back to top</a>)</p>


