# Flask_Call_List_Upload

## Описание проекта

Это Flask-приложение предоставляет REST API для:
1. **Загрузки и валидации колл-листов** на разных голосовых ассистентов.
2. **Отправки результатов** обработки данных на заданный URL.

Приложение выполняет валидацию входящих данных, рефакторинг содержимого и логирование действий, предоставляя надёжный инструмент для обработки и мониторинга колл-листов.

---

## Основные возможности

- **Загрузка колл-листов**: 
  - Эндпоинт `/bulk_upload` принимает JSON-данные, выполняет валидацию и рефакторинг, а затем загружает их для дальнейшей обработки.
- **Отправка результатов**:
  - Эндпоинт `/send_results` отправляет обработанные результаты на указанный URL.
- **Валидация входящих данных**
  - Проверяет корректность формата данных и наличие всех необходимых полей.
- **Логирование и уведомления**:
  - Все запросы и ключевые события логируются. Ошибки отправляются в Telegram для быстрого реагирования.

---
