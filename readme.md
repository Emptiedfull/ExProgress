# ExProgress

The perfect way to pass time while watching your 200gb file transfer go through

ExProgress is a demonstration based on the xkcd comic "Backwards in Time". It features a progress bar that represents different periods in history, with each point on the progress bar corresponding to a specific time in history.

[Click here to expereince]()

## Installation



1. Clone the repository:
    ```sh
    git clone https://github.com/Emptiedfull/ExProgress
    ```
2. Navigate to the project directory:
    ```sh
    cd exprogress
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Running the web demo

1. Start the server:

        ```sh
        python server.py
        ```

    or for more control

        ```sh
        uvicorn server:app --port <port> 
        ```
   
2. Open your web browser and navigate to `http://localhost:<port>`.

### Using as a Lib

The code in /bar_utils exposes all the neccesary functions for using the tool.

1. **conversion.py**: Converts progress values to years format

2. **map.py**: contains the code for converting         formula     output to human readable format

3. **ai.py**: contains the code for generating time period descriptions. An anthropic api key must be provided in .env for this to work.

4. **locate.py**: contains code to search and locate values based on progress from an existing lookup table. Check mappings.json for example

5. **utils.py**: useful code for sanitzing n sorting lookup table.






## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [xkcd](https://xkcd.com/) for the original comic inspiration.
- [Claude AI](https://claude.ai) for generating descriptions of time periods.
- [GitHub Copilot](https://github.com/features/copilot) for assisting with code suggestions.