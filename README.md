# Chatbot for Whatsapp

> A fully functional conversational chatbot for your buisness integrated with whatsapp.  

## Installation

Folow these steps to setup the project:
  
1. Set up the Google Cloud Platform sdk in your machine
2. Create a project and authenticate the terminal (needed to deploy to cloud)
3. Set up a twilio account and a facebook buisness number
3. All in one setup (`setup.bat`)

The support is only currently working for windows but you can use the .bat scripts to generate your .sh.
If you cant to debugg the process manually follow the next commands:

```sh
./install_dependecies.bat
python createSecrets.py
./deploy_to_gcloud.bat
```
  
## Usage example

Create your own secrets.json file and run:
```
setup.bat
```

 

  

## Release History  

  

* 0.1
* Work in progress

  

## Meta

  

David Ramirez – [@JuanDav80657184]([https://twitter.com/JuanDav80657184](https://twitter.com/JuanDav80657184))

Contact me [here]([https://david.alfagenos.com/contact](https://david.alfagenos.com/contact)) 

  

## Contributing

  

1. Fork it (<[https://github.com/juanda2222/playground/fork](https://github.com/juanda2222/playground/fork)>)

2. Create your feature branch (`git checkout -b feature/fooBar`)

3. Commit your changes (`git commit -am 'Add some fooBar'`)

4. Push to the branch (`git push origin feature/fooBar`)

5. Create a new Pull Request