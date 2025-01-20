import flet as ft
import zipfile
import os
import sys
import requests

pyData1 = sys.copyright
cpuData1 = os.cpu_count()

def main(page: ft.Page):
    page.title = "Xzip Installer"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    

    def read_txt_file(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read()
                return text
        except FileNotFoundError:
            return "ERROR 404_1: Файл не найден."
        except Exception as e:
            return f"ERROR 1: {e}"

    def unzip_to_folder(zip_filepath, destination_folder):
        try:
            with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                os.makedirs(destination_folder, exist_ok=True)
                zip_ref.extractall(destination_folder)
            return True
        except FileNotFoundError:
            return "ERROR 404_2: ZIP-архив не найден."
        except zipfile.BadZipFile:
            return "ERROR 2: Неверный формат ZIP-архива."
        except Exception as e:
            return f"ERROR 3: {e}"

    def add_log(message):
        log_console.value += f"{message}\n"
        page.update()

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            page.update()
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.update()

    def install_clicked(e):
        if agreement_checkbox.value:
            add_log("Начало установки...")
            result = unzip_to_folder(zip_file, destination_folder)
            if isinstance(result, str):  # Проверка на наличие ошибки
                output_text.value = f"Ошибка: {result}"
                add_log(f"Ошибка: {result}")
            else:
                output_text.value = "Архив распакован. Файл в папке Загрузки."
                add_log("Установка завершена успешно.")
            page.update()
        else:
            output_text.value = "Вы должны согласиться с лицензионным соглашением для установки."
            page.update()

    def update(e):
        add_log("Начало обновления...")
        license_filepath = os.path.join(script_dir, "Data/updater.txt") 
        license_text = """
        При обновлении мы не обещаем, что загруженный файл будет работать!
        Package URL = https://raw.githubusercontent.com/SasiskaMine/Xzip-Installer/download/Installer.py
        """

        if license_text:
            output_text.value = f"\nИнформация:\n{license_text}"
            page.update()  # Используйте глобальную переменную page
            output_text.value += "Вы согласны с установкой обновления? (Y/N):"
            page.update()

        # Логика для загрузки файла и обновления
        url = "https://raw.githubusercontent.com/SasiskaMine/Xzip-Installer/download/Installer.py" 
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            installer_filepath = os.path.join(script_dir, "Installer.py")  
            with open(installer_filepath, 'wb') as f:  
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    progress_bar.value += len(chunk) / response.headers.get('content-length', 1)
                    page.update()

            output_text.value = "Обновление установлено! Для запуска снова зайдите в Installer.py"
            add_log("Обновление завершено успешно.")
            page.update()

        except requests.exceptions.RequestException as e:
            output_text.value = f"Ошибка при скачивании файла: {e}"
            add_log(f"Ошибка при скачивании файла: {e}")
            page.update()

    def show_settings(e):
        # Отображаем версию и поле для выбора пути
        settings_text = f"Версия Xzip Installer: 1.1.1"
        output_text.value = settings_text
        page.update()

        # Поле для выбора пути
        path_input = ft.TextField(label="Выберите путь для сохранения файла", value=destination_folder)
        page.add(path_input)

        # Кнопка для подтверждения выбора пути
        confirm_button = ft.ElevatedButton(text="Подтвердить", on_click=lambda e: confirm_path(path_input.value))
        page.add(confirm_button)

    def confirm_path(selected_path):
        global destination_folder
        destination_folder = selected_path
        output_text.value = f"Путь для сохранения файла изменен на: {destination_folder}"
        page.update()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    archive_name = "Data/Image.zip"
    zip_file = os.path.join(script_dir, archive_name)
    destination_folder = os.path.join(script_dir, "Downloads")
    license_filepath = os.path.join(script_dir, "Data/info.txt")
    license_text = read_txt_file(license_filepath)

    agreement_checkbox = ft.Checkbox(label="Я согласен с лицензионным соглашением", value=False)
    install_button = ft.ElevatedButton(text="Установить", on_click=install_clicked, disabled=False)
    update_button = ft.ElevatedButton(text="Обновить Xzip Installer", on_click=update, disabled=True)
    output_text = ft.Text("", size=12)  # Изменено на размер шрифта в пикселях

    def agreement_changed(e):
        install_button.disabled = not e.control.value
        update_button.disabled = not e.control.value  # Активируем кнопку обновления
        page.update()

    agreement_checkbox.on_change = agreement_changed

    # Добавляем кнопку настроек
    settings_button = ft.ElevatedButton(text="Настройки", on_click=show_settings, disabled=True)
    
    # Добавляем консоль для логов
    log_console = ft.TextField(label="Console", value="", read_only=True, multiline=True, height=200, width=400)

    # Добавляем прогресс-бар
    progress_bar = ft.ProgressBar(width=400)

    # Кнопка для смены темы
    theme_button = ft.ElevatedButton(text="Сменить тему", on_click=toggle_theme)

    page.add(
        ft.AppBar(
            title=ft.Text("Xzip Installer 1.4", size=ft.TextSpan, weight=ft.FontWeight.BOLD),
            bgcolor=ft.colors.BLUE,
            actions=[
                ft.IconButton(icon=ft.icons.LIGHT_MODE, on_click=toggle_theme),
            ],
        ),
        ft.Column(
            [
                ft.Divider(),
                ft.Text(license_text if license_text else "Не удалось загрузить лицензионное соглашение.", selectable=True),
                agreement_checkbox,
                install_button,
                output_text,
                update_button,
                settings_button,  # Кнопка настроек не работает
                progress_bar,  # Добавляем прогресс-бар
                log_console,  # Добавляем консоль для логов
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            
        )
        
    )
    if cpuData1 == 1:
        page.add(ft.Text("Ошибка 5: Ошибка ЦП", color=ft.colors.RED))

ft.app(target=main)
