import os
import secrets


def create_env_file():
    prompt = "> "
    if os.path.exists(".env"):
        print(".env Datei exisiter bereits.")
    else:
        

        print("REDIS_PW= ?")
        REDIS_PW = input(prompt)

        
        SECRET_KEY = secrets.token_hex(32)
        JWT_SECRET = secrets.token_hex(32)

        env_list = [
            "DATABASE={}\n".format("app"),
            "REDIS_PW={}\n".format(REDIS_PW),
            "SECRET_KEY={}\n".format(SECRET_KEY),
            "JWT_SECRET={}\n".format(JWT_SECRET),
        ]

        with open(os.path.join('.env'), 'a') as f:
            [ f.write(env_var) for env_var in env_list ]
            f.close()


def main():
    create_env_file()


if __name__ == '__main__':
main()