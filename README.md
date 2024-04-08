# Plagiarism finder

## 한국어 버전을 찾고 계신가요?
[한국어 버전](README_kr.md)

## Description
This program is a program that analyzes the similarity of text, document, and code files.
The currently supported file formats are as follows.

- Documents (Only image check is supported, under development)
```text
docx,pdf
```
- Code (Under development)
```text
c, cpp, h, hpp, py, java, mat, m, cs, asm, js, v, vhd, vhdl, r
```
- Text (Under development)
```textNeurIPS
txt, csv, json, xml, html, css, yml, yaml
```

## File structure
```text
src/
├── common.py
├── config.py
├── main.py
tools/
├── compare/
│   ├── code.py
│   ├── image.py
│   ├── text.py
├── extract/
│   ├── parse_files.py
├── transform.py
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

## Note
- The program is currently under development and may not work properly.
- This program is intended to be used as a tool to assist in the detection of plagiarism. It is not a substitute for human judgment, and it is not a guarantee of plagiarism. It is the responsibility of the user to verify the results and determine whether plagiarism has occurred. The authors of this program are not responsible for any consequences that may arise from the use of this program.

## Todo
- [ ] Improve image comparison efficiency
    - [ ] Speed up image comparison by image compression
    - [ ] Compute similarity using block matrix inner product
- [ ] Implement document comparison
- [ ] Implement code comparison
- [ ] Implement text comparison

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributions Welcome!
Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests. If you have any suggestions for improvement or new features, please let us know.

## Contact
If you have any questions or need further assistance, please contact us at the following:
- Email: [jwlee@linux.com](mailto:jwlee@linux.com)
- Issue Tracker: [GitHub Issues](https://github.com/metr0jw/Plagiarism-finder/issues)
- Discussion Forum: [GitHub Discussions](https://github.com/metr0jw/Plagiarism-finder/discussions)

## Authors
- [**Jangsoo Park**](https://github.com/jangsoopark) - *Initial work*
- [**Jiwoon Lee**](https://github.com/metr0jw) - *Initial work*, *Maintainer*

## Thanks
- [**Jihyun Ha**](https://github.com/j2hxxx) - *Beta tester*
