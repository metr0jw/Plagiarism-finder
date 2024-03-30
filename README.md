# Plagiarism finder - Kwangwoon University
## Department of Computer Engineering

## 프로그램 설명
본 프로그램은 텍스트, 문서, 코드 파일을 입력받아 유사도를 분석하는 프로그램입니다.
현재 지원하는 파일 형식은 다음과 같습니다.

- 문서 파일
```text
docx,pdf
```
- 코드 파일
```text
c, cpp, h, hpp, py, java, mat, m, cs, asm, js, v, vhd, vhdl, r
```
- 텍스트 파일
```text
txt, csv, json, xml, html, css, yml, yaml
```

## 파일 구조
```text
src/
├── common.py
├── main.py
tools/
├── extract_images_from_doc.py
README.md
requirements.txt
```

## 사용법
```bash