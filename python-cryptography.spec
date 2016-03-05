#
# Conditional build:
%bcond_without  python2 # CPython 2.x module
%bcond_without  python3 # CPython 3.x module

Summary:	Crypthography library for Python 2
Summary(pl.UTF-8):	Biblioteka Cryptography dla Pythona 2
Name:		python-cryptography
Version:	1.2.3
Release:	3
License:	Apache v2.0 or BSD
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/c/cryptography/cryptography-%{version}.tar.gz
# Source0-md5:	5474d2b3e8c7555a60852e48d2743f85
URL:		https://cryptography.io/
BuildRequires:	openssl-devel >= 0.9.8
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-cffi >= 1.4.1
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-enum34
BuildRequires:	python-pyasn1 >= 0.1.8
BuildRequires:	python-setuptools
BuildRequires:	python-six >= 1.4.1
%endif
%if %{with python3}
BuildRequires:	python3-cffi >= 1.4.1
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-pyasn1 >= 0.1.8
BuildRequires:	python3-setuptools
BuildRequires:	python3-six >= 1.4.1
%endif
Requires:	python-cffi >= 1.4.1
Requires:	python-six >= 1.4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cryptography is a package designed to expose cryptographic recipes and
primitives to Python developers. Our goal is for it to be your
"cryptographic standard library". It supports Python 2.6-2.7, Python
3.2+, and PyPy.

cryptography includes both high level recipes, and low level
interfaces to common cryptographic algorithms such as symmetric
ciphers, message digests and key derivation functions.

This package contains Python 2 modules.

%description -l pl.UTF-8
cryptography to pakiet zaprojektowany w celu udostępnienia funkcji i
obiektów kryptograficznych programistom Pythona. Celem jest
dostarczenie "standardowej biblioteki kryptograficznej". Obsługuje
Pythona 2.6-2.7, Pythona 3.2+ oraz PyPy.

cryptography zawiera zarówno funkcje wysokopoziomowe, jak i
niskopoziomowe interfejsy do popularnych algorytmów kryptograficznych,
takich jak szyfry symetryczne, skróty wiadomości czy funkcje
wyprowadzające klucze.

Ten pakiet zawiera moduły Pythona 2.

%package -n python3-cryptography
Summary:	Crypthography library for Python 3
Summary(pl.UTF-8):	Biblioteka Cryptography dla Pythona 3
Group:		Libraries/Python
Requires:	python3-cffi >= 1.4.1
Requires:	python3-six >= 1.4.1

%description -n python3-cryptography
cryptography is a package designed to expose cryptographic recipes and
primitives to Python developers. Our goal is for it to be your
"cryptographic standard library". It supports Python 2.6-2.7, Python
3.2+, and PyPy.

cryptography includes both high level recipes, and low level
interfaces to common cryptographic algorithms such as symmetric
ciphers, message digests and key derivation functions.

This package contains Python 3 modules.

%description -n python3-cryptography -l pl.UTF-8
cryptography to pakiet zaprojektowany w celu udostępnienia funkcji i
obiektów kryptograficznych programistom Pythona. Celem jest
dostarczenie "standardowej biblioteki kryptograficznej". Obsługuje
Pythona 2.6-2.7, Pythona 3.2+ oraz PyPy.

cryptography zawiera zarówno funkcje wysokopoziomowe, jak i
niskopoziomowe interfejsy do popularnych algorytmów kryptograficznych,
takich jak szyfry symetryczne, skróty wiadomości czy funkcje
wyprowadzające klucze.

Ten pakiet zawiera moduły Pythona 3.

%prep
%setup -q -n cryptography-%{version}

%build
export CFLAGS="%{rpmcflags}"

%if %{with python2}
%py_build \
	--build-base build-2
%endif

%if %{with python2}
%py3_build \
	--build-base build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS.rst README.rst LICENSE.APACHE LICENSE.BSD
%dir %{py_sitedir}/cryptography
%{py_sitedir}/cryptography/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat
%{py_sitedir}/cryptography/hazmat/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/backends
%{py_sitedir}/cryptography/hazmat/backends/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/backends/commoncrypto
%{py_sitedir}/cryptography/hazmat/backends/commoncrypto/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/backends/openssl
%{py_sitedir}/cryptography/hazmat/backends/openssl/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/bindings
%{py_sitedir}/cryptography/hazmat/bindings/*.py[co]
%attr(755,root,root) %{py_sitedir}/cryptography/hazmat/bindings/_*.so
%dir %{py_sitedir}/cryptography/hazmat/bindings/commoncrypto
%{py_sitedir}/cryptography/hazmat/bindings/commoncrypto/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/bindings/openssl
%{py_sitedir}/cryptography/hazmat/bindings/openssl/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/primitives/interfaces
%{py_sitedir}/cryptography/hazmat/primitives/interfaces/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/primitives
%{py_sitedir}/cryptography/hazmat/primitives/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/primitives/asymmetric
%{py_sitedir}/cryptography/hazmat/primitives/asymmetric/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/primitives/ciphers
%{py_sitedir}/cryptography/hazmat/primitives/ciphers/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/primitives/kdf
%{py_sitedir}/cryptography/hazmat/primitives/kdf/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/primitives/twofactor
%{py_sitedir}/cryptography/hazmat/primitives/twofactor/*.py[co]
%dir %{py_sitedir}/cryptography/x509
%{py_sitedir}/cryptography/x509/*.py[co]
%{py_sitedir}/cryptography-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-cryptography
%defattr(644,root,root,755)
%doc AUTHORS.rst README.rst LICENSE.APACHE LICENSE.BSD
%dir %{py3_sitedir}/cryptography
%{py3_sitedir}/cryptography/*.py
%{py3_sitedir}/cryptography/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat
%{py3_sitedir}/cryptography/hazmat/*.py
%{py3_sitedir}/cryptography/hazmat/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/backends
%{py3_sitedir}/cryptography/hazmat/backends/*.py
%{py3_sitedir}/cryptography/hazmat/backends/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/backends/commoncrypto
%{py3_sitedir}/cryptography/hazmat/backends/commoncrypto/*.py
%{py3_sitedir}/cryptography/hazmat/backends/commoncrypto/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/backends/openssl
%{py3_sitedir}/cryptography/hazmat/backends/openssl/*.py
%{py3_sitedir}/cryptography/hazmat/backends/openssl/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/bindings
%{py3_sitedir}/cryptography/hazmat/bindings/*.py
%{py3_sitedir}/cryptography/hazmat/bindings/__pycache__
%attr(755,root,root) %{py3_sitedir}/cryptography/hazmat/bindings/_*.so
%dir %{py3_sitedir}/cryptography/hazmat/bindings/commoncrypto
%{py3_sitedir}/cryptography/hazmat/bindings/commoncrypto/*.py
%{py3_sitedir}/cryptography/hazmat/bindings/commoncrypto/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/bindings/openssl
%{py3_sitedir}/cryptography/hazmat/bindings/openssl/*.py
%{py3_sitedir}/cryptography/hazmat/bindings/openssl/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/primitives/interfaces
%{py3_sitedir}/cryptography/hazmat/primitives/interfaces/*.py
%{py3_sitedir}/cryptography/hazmat/primitives/interfaces/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/primitives
%{py3_sitedir}/cryptography/hazmat/primitives/*.py
%{py3_sitedir}/cryptography/hazmat/primitives/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/primitives/asymmetric
%{py3_sitedir}/cryptography/hazmat/primitives/asymmetric/*.py
%{py3_sitedir}/cryptography/hazmat/primitives/asymmetric/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/primitives/ciphers
%{py3_sitedir}/cryptography/hazmat/primitives/ciphers/*.py
%{py3_sitedir}/cryptography/hazmat/primitives/ciphers/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/primitives/kdf
%{py3_sitedir}/cryptography/hazmat/primitives/kdf/*.py
%{py3_sitedir}/cryptography/hazmat/primitives/kdf/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/primitives/twofactor
%{py3_sitedir}/cryptography/hazmat/primitives/twofactor/*.py
%{py3_sitedir}/cryptography/hazmat/primitives/twofactor/__pycache__
%dir %{py3_sitedir}/cryptography/x509
%{py3_sitedir}/cryptography/x509/*.py
%{py3_sitedir}/cryptography/x509/__pycache__
%{py3_sitedir}/cryptography-%{version}-py*.egg-info
%endif
