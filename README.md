## About The Project

The Post Organizer is a Flask web application that implements a simple, file-based, publish-subscribe service. The service operates as a push-pull system that uses a set of catch-all routes for post and get requests. A post request posts a payload to a box while a get request pops a payload from the web application. The URI of the request is used to select the "box" that the payload is going to be delivered to or retrieved from. To protect the local file system from enumeration, the URI is tokenized with the resulting tokens being converted to hash strings. A specified root directory for the boxes and hashed tokens from the URI are used to resolve a requested box.

Posting a payload to `http://localhost:8080/8` results in the following on the file system:
`./boxes/2c624232cdd221771294dfbb310aca000a0df6ac8b66b696d90ef06fdefb64a3/3a29ca05844085a8b328376b6cc73bb4ce6f848dc72ac50730bcead2e252de7a`.

When getting a payload from `http://localhost:8080/8`, a file is read from the box (`./boxes/2c624232cdd221771294dfbb310aca000a0df6ac8b66b696d90ef06fdefb64a3`) and both served in the HTTP response and deleted from the file system. If payloads are left in the box for a configured amount of time, they are considered expired and are simply deleted. Any box directory or child directory that is empty is also removed as part of the expiration process.

## Getting Started

### Prerequisites

* Python 3.10
* Python Pip
* Docker (for integration testing)

### Installation

Do the steps below to setup and run the project locally.

1. Clone the repo
   ```sh
   git clone https://github.com/phnomcobra/posts-organizer.git
   ```
2. Install requirements
   ```sh
   pip install -r requirements.txt
   ```
3. Run flask application
   ```sh
   python3 main.py
   ```

### Integration Testing

Do the steps below to spin up a docker environment. A server, consumer, and producer are established for demonstating the posting and getting items from a box, expiration of posts and box child directories, and logging behavior.

1. Install Docker or Docker Desktop
2. Install Docker Compose
3. Clone the repo
   ```sh
   git clone https://github.com/phnomcobra/posts-organizer.git
   ```
4. Run the compose file
   ```sh
   docker-compose up
   ```

## Notes

There is a hard dependency on Python 3.10 because of the "NoneTypes" in the pydantic defaults. To run on earlier versions of Python 3, remove the none-equals-default values from the pydantic classes.

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.
