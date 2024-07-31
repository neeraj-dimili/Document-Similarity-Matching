from db_config import DbConfig
from train_test import train, test


def main():
    DbConfig.setup()
    train()
    test()
    DbConfig.close_connection()


if __name__ == "__main__":
    main()
