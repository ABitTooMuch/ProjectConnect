# ProjectConnect
## How to run server:
1. Pull the project and navigate to the base directory containing the requirements.txt
2. Create a virtual environment
    
    ```
    $ virtualenv <venv_name>
    ```
3. Activate the virtual environment
    
    Windows
    ```
    $ .\<venv_name>\scripts\activate
    ```
    
    Unix/Linux
    ```
    $ . <venv_name>/bin/activate
    ```
    
    If successful your prompt will look something like this:
    
    ```
    (<venv_name>)$
    ```
4. Install the project dependencies
    
    ```
    $ pip install -r requirements.txt
    ```

5. Create the database

    ```
    $ flask db upgrade
    ```
    

6. Start the service

    Windows
    ```
    $ projectconnect.py
    ```

    Linux/Unix/Windows
    ```
    $ python projectconnect.py
    ```


7. Navigate to http://localhost:4000 in your browser

## Project Structure

    ProjectConnect/
        app/
            auth/ - contains code and routes (not templates) related to login and authentication
                forms.py
                routes.py
            main/ - contains all the main site logic and endpoints
                forms.py
                routes.py
            dev/ - development version of the site
            models/ - contains all of the database models
                user.py - contains user model
                project.py - contains project model
                tables.py - contains relational tables
                attributes.py - attributes like tags and skills
            templates/ - contains the templates for all pages
                dev/ - templates only used for backend develeopment
            static/ (Non-existent) - this is where all static content (images, js, css) for templates should go
        migrations/ - automatically created; database table information
        projectconnect.py - entrypoint for the project. Run this to start the service
        tests.py - unit tests
        config.py - configuration variables for the project
