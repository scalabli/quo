from quo import prompt
if __name__ == "__main__":
    answer = prompt("Give me some input: ")
    answer = answer.encode("utf-8",errors='surrogateescape').decode('utf-8')
    print("You said: %s" % answer)
