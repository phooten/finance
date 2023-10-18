import class_messages

msg = class_messages.messages()

def testing():
    msg.error( "error message here.", __name__ )
    msg.warning( "warning message here.", __name__ )
    msg.system( "normal message here.", __name__ )
    msg.quit_script()
    return



def main():
    testing()
    return

if __name__ == "__main__":
    main()
