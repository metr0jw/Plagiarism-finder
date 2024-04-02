# 표절 검사기 - 광운대학교 컴퓨터공학과

## Are you looking for English version?
[English version](README.md)

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

## 사용 방법
1. (선택) 가상 환경을 생성합니다.
```bash
python -m venv VIRTUAL_ENV_NAME
source VIRTUAL_ENV_NAME/bin/activate
```

2. 필요한 패키지를 설치합니다.
```bash
pip install -r requirements.txt
```

3. 비교하고 싶은 파일(예: 소스 코드, 문서, 텍스트)을 `submission` 디렉토리에 넣습니다.
```text
submission/
├── studentname/
│   ├── code1.cpp
│   ├── code2.cpp
│   ├── report.docx
│   ├── report.pdf
├── couldbeanyname/
│   ├── code1.cpp
│   ├── code2.java
│   ├── code3.py
│   ├── report.pdf
```

4. (선택) 이전에 제출된 과제가 있다면, `reference` 디렉토리에 넣습니다.
```text
reference/
├── prev_studentname/
│   ├── code1.cpp
│   ├── code2.cpp
│   ├── report.docx
│   ├── report.pdf
├── prev_studentname2/
│   ├── code1.cpp
│   ├── code2.java
│   ├── code3.py
│   ├── report.pdf
```

5. 프로그램을 실행합니다.
```bash
python src/main.py
```

6. 결과는 `result` 디렉토리에 저장됩니다.
```text
result/
├── result.csv
```

## 라이센스
이 프로젝트는 MIT 라이센스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 기여를 환영합니다!
이 프로젝트에 기여하고 싶으시다면, 이 저장소를 fork하고 pull request를 생성해주세요.

## 문의
만약 궁금한 점이 있으시다면, 아래 이메일 주소로 연락해주세요.
```python
email = "jwlee@linux.com"
```

## 저자
- **박장수** - *초기 작업* - [박장수](https://github.com/jangsoopark), 광운대학교 컴퓨터공학과
- **이지운** - *초기 작업* - [이지운](https://github.com/metr0jw), 광운대학교 컴퓨터공학과
