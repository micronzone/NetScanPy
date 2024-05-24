# NetScanPy

NetScanPy는 Python으로 작성된 네트워크 스캐닝 도구입니다. 이 프로젝트는 네트워크 보안 관리자나 시스템 관리자들이 네트워크에 대한 정보를 수집하고 보안 취약점을 확인하는 데 도움을 줍니다. 이 도구는 `nmap`을 기반으로 하며, 사용자 친화적으로 안내되는 옵션에 따라 다양한 스캔을 실행할 수 있습니다.

### 배경

네트워크를 지속적으로 모니터링하면서 자주 사용하는 옵션을 간편하게 실행하는 스캐닝 도구가 필요했는데, NetScanPy는 이러한 요구에 부합하여 만들게 되었습니다.

## 기능

- macOS, Linux, Windows 크로스플랫폼 지원
- 다양한 `nmap` 옵션을 사용하여 네트워크 스캔 실행
- 수동으로 IP 주소 입력 또는 로컬 네트워크 스캔을 통한 대상 선택
- 스캔 결과를 실시간으로 확인
- 사용자 친화적인 CLI 인터페이스 제공

## 설치 방법

1. 프로젝트를 클론합니다:

    ```bash
    git clone https://github.com/micronzone/NetScanPy.git
    cd NetScanPy
    ```

2. (선택 사항) 가상 환경을 생성하고 활성화합니다:
    ```sh
    python3 -m venv myenv
    source myenv/bin/activate  # Linux 또는 macOS
    .\myenv\Scripts\activate   # Windows
    ```

3. 필요한 라이브러리를 설치합니다:
    ```sh
    pip3 install -r requirements.txt
    ```
    또는 `tqdm>=4.62.3`
    ```sh
    pip3 install tqdm
    ```

## 사용 방법

대화형 실행
```sh
python3 netscanpy.py
```

빠른 스캔 실행
```sh
python3 netscanpy.py [옵션]
```

### 옵션

- `-l` : 모든 스캐닝 옵션 번호
- `-n {1, 2, ..}` : 스캐닝 옵션 번호를 선택하여 빠른 실행 (예: 8번 옵션 선택하려면 `-n 8`)
- `-h, --help` : NetScanPy 도움말

### 예시

Nmap 스캐닝 옵션을 대화형으로 실행하는 예시입니다:
```sh
python3 netscanpy.py
```

빠른 스캔을 위해 Nmap 스캐닝 옵션을 출력하는 예시입니다:
```sh
python3 netscanpy.py -l
```

빠른 스캔을 위해 Nmap 스캐닝 옵션을 사용하여 실행하는 예시입니다:
```sh
python3 netscan.py -n 8
```

## 업데이트

NetScanPy 리포지토리 업데이트를 확인하는 것이 좋습니다!

```sh
cd NetScanPy
git status
```

변경 사항 가져오기:

```sh
git pull origin main
```

## 기여 방법

기여해주셔서 감사합니다! 이 프로젝트에 기여하시려면 아래 단계를 따라 주세요:

1. 이 리포지토리를 포크하세요
2. 기능 브랜치(micronzone 브랜치)를 생성하세요 (`git checkout -b micronzone/NetScanPy`)
3. 변경 사항을 커밋하세요 (`git commit -m 'Add some NetScanPy'`)
4. 브랜치에 푸시하세요 (`git push origin micronzone/NetScanPy`)
5. 풀 리퀘스트를 여세요

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.
