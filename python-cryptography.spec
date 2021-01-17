#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit test

Summary:	Crypthography library for Python 2
Summary(pl.UTF-8):	Biblioteka Cryptography dla Pythona 2
Name:		python-cryptography
Version:	3.3.1
Release:	1
License:	Apache v2.0 or BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cryptography/
Source0:	https://files.pythonhosted.org/packages/source/c/cryptography/cryptography-%{version}.tar.gz
# Source0-md5:	6faa1a7125c500c0e1586ad342ba3b30
#Source1Download: https://pypi.org/simple/cryptography_vectors/
Source1:	https://files.pythonhosted.org/packages/source/c/cryptography-vectors/cryptography_vectors-%{version}.tar.gz
# Source1-md5:	2a23fd073fc1f95a697ee96fc991e419
URL:		https://cryptography.io/
BuildRequires:	openssl-devel >= 1.1.0
BuildRequires:	rpm-pythonprov >= 5.4.15-48
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-cffi >= 1.12
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-enum34
BuildRequires:	python-pytz
BuildRequires:	python-setuptools >= 18.5
BuildRequires:	python-six >= 1.4.1
%if %{with tests}
%if "%{py_ver}" >= "2.7"
BuildRequires:	python-hypothesis >= 1.11.4
%endif
BuildRequires:	python-ipaddress
BuildRequires:	python-iso8601
BuildRequires:	python-pretend
BuildRequires:	python-pytest >= 3.6.0
BuildRequires:	python-pytz
%endif
%endif
%if %{with python3}
BuildRequires:	python3-cffi >= 1.12
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-setuptools >= 18.5
BuildRequires:	python3-six >= 1.4.1
%if %{with tests}
BuildRequires:	python3-hypothesis >= 1.11.4
BuildRequires:	python3-iso8601
BuildRequires:	python3-pretend
BuildRequires:	python3-pytest >= 3.6.0
BuildRequires:	python3-pytz
%endif
%endif
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3 >= 1.6.5
%endif
Requires:	openssl >= 1.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cryptography is a package designed to expose cryptographic recipes and
primitives to Python developers. Our goal is for it to be your
"cryptographic standard library". It supports Python 2.7, Python 3.4+,
and PyPy.

cryptography includes both high level recipes, and low level
interfaces to common cryptographic algorithms such as symmetric
ciphers, message digests and key derivation functions.

This package contains Python 2 modules.

%description -l pl.UTF-8
cryptography to pakiet zaprojektowany w celu udostępnienia funkcji i
obiektów kryptograficznych programistom Pythona. Celem jest
dostarczenie "standardowej biblioteki kryptograficznej". Obsługuje
Pythona 2.7, Pythona 3.4+ oraz PyPy.

cryptography zawiera zarówno funkcje wysokopoziomowe, jak i
niskopoziomowe interfejsy do popularnych algorytmów kryptograficznych,
takich jak szyfry symetryczne, skróty wiadomości czy funkcje
wyprowadzające klucze.

Ten pakiet zawiera moduły Pythona 2.

%package -n python3-cryptography
Summary:	Crypthography library for Python 3
Summary(pl.UTF-8):	Biblioteka Cryptography dla Pythona 3
Group:		Libraries/Python
Requires:	openssl >= 1.1.0

%description -n python3-cryptography
cryptography is a package designed to expose cryptographic recipes and
primitives to Python developers. Our goal is for it to be your
"cryptographic standard library". It supports Python 2.7, Python 3.4+,
and PyPy.

cryptography includes both high level recipes, and low level
interfaces to common cryptographic algorithms such as symmetric
ciphers, message digests and key derivation functions.

This package contains Python 3 modules.

%description -n python3-cryptography -l pl.UTF-8
cryptography to pakiet zaprojektowany w celu udostępnienia funkcji i
obiektów kryptograficznych programistom Pythona. Celem jest
dostarczenie "standardowej biblioteki kryptograficznej". Obsługuje
Pythona 2.7, Pythona 3.4+ oraz PyPy.

cryptography zawiera zarówno funkcje wysokopoziomowe, jak i
niskopoziomowe interfejsy do popularnych algorytmów kryptograficznych,
takich jak szyfry symetryczne, skróty wiadomości czy funkcje
wyprowadzające klucze.

Ten pakiet zawiera moduły Pythona 3.

%package apidocs
Summary:	API documentation for cryptography module
Summary(pl.UTF-8):	Dokumentacja API modułu cryptography
Group:		Documentation
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description apidocs
API documentation for cryptography module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu cryptography.

%prep
%setup -q -n cryptography-%{version} %{?with_tests:-a1}

%if %{with tests}
%{__mv} cryptography_vectors-%{version}/cryptography_vectors .
%endif

%build
export CFLAGS="%{rpmcflags}"

%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-2/lib.*) \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
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
%doc AUTHORS.rst README.rst LICENSE LICENSE.APACHE LICENSE.BSD
%dir %{py_sitedir}/cryptography
%{py_sitedir}/cryptography/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat
%{py_sitedir}/cryptography/hazmat/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/backends
%{py_sitedir}/cryptography/hazmat/backends/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/backends/openssl
%{py_sitedir}/cryptography/hazmat/backends/openssl/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/bindings
%{py_sitedir}/cryptography/hazmat/bindings/*.py[co]
%attr(755,root,root) %{py_sitedir}/cryptography/hazmat/bindings/_*.so
%dir %{py_sitedir}/cryptography/hazmat/bindings/openssl
%{py_sitedir}/cryptography/hazmat/bindings/openssl/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/primitives
%{py_sitedir}/cryptography/hazmat/primitives/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/primitives/asymmetric
%{py_sitedir}/cryptography/hazmat/primitives/asymmetric/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/primitives/ciphers
%{py_sitedir}/cryptography/hazmat/primitives/ciphers/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/primitives/kdf
%{py_sitedir}/cryptography/hazmat/primitives/kdf/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/primitives/serialization
%{py_sitedir}/cryptography/hazmat/primitives/serialization/*.py[co]
%dir %{py_sitedir}/cryptography/hazmat/primitives/twofactor
%{py_sitedir}/cryptography/hazmat/primitives/twofactor/*.py[co]
%dir %{py_sitedir}/cryptography/x509
%{py_sitedir}/cryptography/x509/*.py[co]
%{py_sitedir}/cryptography-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-cryptography
%defattr(644,root,root,755)
%doc AUTHORS.rst README.rst LICENSE LICENSE.APACHE LICENSE.BSD
%dir %{py3_sitedir}/cryptography
%{py3_sitedir}/cryptography/*.py
%{py3_sitedir}/cryptography/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat
%{py3_sitedir}/cryptography/hazmat/*.py
%{py3_sitedir}/cryptography/hazmat/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/backends
%{py3_sitedir}/cryptography/hazmat/backends/*.py
%{py3_sitedir}/cryptography/hazmat/backends/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/backends/openssl
%{py3_sitedir}/cryptography/hazmat/backends/openssl/*.py
%{py3_sitedir}/cryptography/hazmat/backends/openssl/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/bindings
%{py3_sitedir}/cryptography/hazmat/bindings/*.py
%{py3_sitedir}/cryptography/hazmat/bindings/__pycache__
%attr(755,root,root) %{py3_sitedir}/cryptography/hazmat/bindings/_*.so
%dir %{py3_sitedir}/cryptography/hazmat/bindings/openssl
%{py3_sitedir}/cryptography/hazmat/bindings/openssl/*.py
%{py3_sitedir}/cryptography/hazmat/bindings/openssl/__pycache__
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
%dir %{py3_sitedir}/cryptography/hazmat/primitives/serialization
%{py3_sitedir}/cryptography/hazmat/primitives/serialization/*.py
%{py3_sitedir}/cryptography/hazmat/primitives/serialization/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/primitives/twofactor
%{py3_sitedir}/cryptography/hazmat/primitives/twofactor/*.py
%{py3_sitedir}/cryptography/hazmat/primitives/twofactor/__pycache__
%dir %{py3_sitedir}/cryptography/x509
%{py3_sitedir}/cryptography/x509/*.py
%{py3_sitedir}/cryptography/x509/__pycache__
%{py3_sitedir}/cryptography-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_downloads,_static,development,hazmat,x509,*.html,*.js}
%endif
