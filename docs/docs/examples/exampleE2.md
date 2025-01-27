# Importing and exporting data from the abmSHARE server

You can import configuration files or export outputs from simulations by downloading/uploading files with an IDE (Integrated Development Environment) or a common file management or file transfer applications.

Each user with access to the server has a defined `<username>` folder. There is no need to change the path in the input or output files. All paths are defined automatically.

## What to import

In your sandbox folders (`default /home/<username>/sandbox`) there is the `input_files` directory which contains the input configuration files for the abmSHARE model and for input data used by synthetic population module.

The main following import path is 

-  Configuration files path: `/home/<username>/sandbox/input_data`

## What to export
After running a simulation you can export the output to your local machine. The output files are defined in [Sandbox output folder](../examples/exampleE1.md#outputs).

## How to transfer files 
There are several ways how to import and export files depending on your system.
### SCP
For importing or exporting data is reccomended to use the SCP protocol.

#### SCP via WinSCP
For Windows OS you can use [WinSCP](https://winscp.net/). 

#### SCP via terminal
For downloading **single file** from the abmSHARE server to your PC (local host) use 
```shell
    scp username@<servername>:/path/to/file/on/server /path/on/localhost/to/copy
```
For downloading **folders**  from the abmSHARE server to your PC (local host) use 
```shell
    scp -r username@<servername>:/path/to/folder/on/server /path/on/localhost/to/copy
```
For uploading **single file** from your PC (local host) to the abmSHARE server use
```shell
    scp /path/on/localhost/to/copy username@<servername>:/path/to/file/on/server
```
For uploading **folders** from your PC (local host) to the abmSHARE server use
```shell
    scp -r /path/on/localhost/to/copy username@<servername>:/path/to/folder/on/server
```

## Linux Filezilla 
For data transfer in Linux you can use [Filezilla](https://filezilla-project.org/) application.
