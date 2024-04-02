# Plagiarism finder

## 한국어 버전을 찾고 계신가요?
[한국어 버전](README_kr.md)

## Description
This program is a program that analyzes the similarity of text, document, and code files.
The currently supported file formats are as follows.

- Documents
```text
docx,pdf
```
- Code
```text
c, cpp, h, hpp, py, java, mat, m, cs, asm, js, v, vhd, vhdl, r
```
- Text
```text
txt, csv, json, xml, html, css, yml, yaml
```

## File structure
```text
src/
├── common.py
├── main.py
tools/
├── extract_images_from_doc.py
README.md
requirements.txt
```

## How to use
1. (Optional) Create a virtual environment.
```bash
python -m venv VIRTUAL_ENV_NAME
source VIRTUAL_ENV_NAME/bin/activate
```

2. Install the required packages.
```bash
pip install -r requirements.txt
```

3. Place the files you want to compare (ex. source code, document, text) in the `submission` directory.
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

4. (Optional) If you have assignments that previously submitted by students, place them in the `reference` directory.
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
5. Run the program.
```bash
python src/main.py
```

6. The results will be saved in the `result` directory.
```text
result/
├── result.csv
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Welcome to contribute!
If you want to contribute to this project, please fork this repository and create a pull request.

## Contact
If you have any questions, please contact me at the following email address.
```python
email = "jwlee@linux.com"
```

## Authors
- **Jangsoo Park** - *Initial work* - [Jangsoo Park](https://github.com/jangsoopark), Department of Computer Engineering, Kwangwoon University
- **Jiwoon Lee** - *Initial work* - [Jiwoon Lee](https://github.com/metr0jw), Department of Computer Engineering, Kwangwoon University
