import zipfile
import os

print("Xzip Installer 1.0.02")

def read_txt_file(filepath):
    """Читает весь текст из TXT файла и возвращает его как строку."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
            return text
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути {filepath}")
        return None
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return None

def unzip_to_folder(zip_filepath, destination_folder):
    """Распаковывает архив в указанную папку."""
    try:
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            os.makedirs(destination_folder, exist_ok=True)
            zip_ref.extractall(destination_folder)
    except FileNotFoundError:
        print(f"Ошибка: ZIP-архив не найден по пути {zip_filepath}")
        return False # Возвращаем False в случае ошибки
    except zipfile.BadZipFile:
        print(f"Ошибка: Неверный формат ZIP-архива по пути {zip_filepath}")
        return False
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return False
    return True # Возвращаем True в случае успеха


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    archive_name = "Data/Image.iso"

    license_filepath = os.path.join(script_dir, "Data/info.txt") # Путь к лицензионному соглашению
    license_text = read_txt_file(license_filepath)

    if license_text:
        print("\nЛицензионное соглашение:\n", license_text)
        print("Вы согласны с Устоновкой? (Y/N):")
        answer = input().upper()

        if answer == "Y":
            zip_file = os.path.join(script_dir, archive_name)
            destination_folder = os.path.join(script_dir, "Downloads")
            print("Распаковка архива...")

            if unzip_to_folder(zip_file, destination_folder):
                print("Архив распакован.")
            else:
                print("Ошибка при распаковке архива.")

        elif answer == "N":
            print("Выполнение программы завершено.")

        else:
            print("Неверный ввод. Выполнение программы завершено.")

    else:
        print("Не удалось прочитать файл с лицензионным соглашением. Выполнение программы завершено.")

input("Для закрытия устовновки нажмите Enter")
