from typing import Dict

try:
    from app.src.models import Entry
except ImportError:
    from .models import Entry

glossary: Dict[str, Entry] = {
    "vulnerability": Entry(
        name="vulnerability",
        description="Это ошибки в программном обеспечении, случайные или намеренные, которое может быть использовано злоумышленником для нанесения ущерба",
        reference="https://www.cyera.com/glossary/vulnerability"
    ),
    "Open_source": Entry(
        name="Open_source",
        description="программное обеспечение, исходный код которого доступен для свободного просмотра, изучения, изменения и распространения",
        reference="https://itglobal.com/ru-ru/company/glossary/open-source/"
    ),
    "Dependency": Entry(
        name="Dependency",
        description="соотношение между требованиями, при котором требование, от которого зависят другие требования, должно быть, как правило, удовлетворено, чтобы и другие требования могли отвечать своим целям",
        reference="https://safe-surf.ru/glossary/ru/850/"
    ),
      "SBOM": Entry(
        name="SBOM",
        description="перечень зависимостей, файлов, библиотек и других элементов, имеющих отношение к конкретному сервису или инфраструктуре целиком",
        reference="https://habr.com/ru/companies/mws/articles/781602/"
    )
}