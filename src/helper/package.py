def package_enable_logging():
    import logging

    # Configure the root logger to output to console
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler()])  # Logs are sent to the standard output
