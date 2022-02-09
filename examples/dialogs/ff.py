import quo
import time


def worker(set_percentage, log_text):

    percentage = 0
    log_text = quo.echo("djdjdjfjfjfjfjj")
    time.sleep(12)
    import platform
    quo.echo(f"{platform.system()}", fg="red")
    time.sleep(10)
    set_percentage=(percentage + 1)
def main():
    quo.ProgressBox(title="djdj", text="ndjdj", run_callback=worker).run()


if __name__ == "__main__":
    main()
