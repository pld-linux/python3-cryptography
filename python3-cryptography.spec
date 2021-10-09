#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit test

Summary:	Crypthography library for Python 3
Summary(pl.UTF-8):	Biblioteka Cryptography dla Pythona 3
Name:		python3-cryptography
Version:	35.0.0
Release:	0.1
License:	Apache v2.0 or BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cryptography/
Source0:	https://files.pythonhosted.org/packages/source/c/cryptography/cryptography-%{version}.tar.gz
# Source0-md5:	ba34eba3ae36cbf3d2e1ee3239f07732
#Source1Download: https://pypi.org/simple/cryptography_vectors/
Source1:	https://files.pythonhosted.org/packages/source/c/cryptography-vectors/cryptography_vectors-%{version}.tar.gz
# Source1-md5:	8e9d050bd601d1788883fa361c69cf85
URL:		https://cryptography.io/
BuildRequires:	openssl-devel >= 1.1.0
BuildRequires:	rpm-pythonprov >= 5.4.15-48
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	rust
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
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3 >= 1.6.5
%endif
Requires:	openssl >= 1.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cryptography is a package which provides cryptographic recipes and
primitives to Python developers. Our goal is for it to be your
"cryptographic standard library". It supports Python 3.6+ and
PyPy3 7.2+.

cryptography includes both high level recipes and low level interfaces
to common cryptographic algorithms such as symmetric ciphers, message
digests, and key derivation functions.

%description -l pl.UTF-8
cryptography to pakiet zaprojektowany w celu udostępnienia funkcji i
obiektów kryptograficznych programistom Pythona. Celem jest
dostarczenie "standardowej biblioteki kryptograficznej". Obsługuje
Pythona 3.6+ oraz PyPy 7.2+.

cryptography zawiera zarówno funkcje wysokopoziomowe, jak i
niskopoziomowe interfejsy do popularnych algorytmów kryptograficznych,
takich jak szyfry symetryczne, skróty wiadomości czy funkcje
wyprowadzające klucze.

%package apidocs
Summary:	API documentation for cryptography module
Summary(pl.UTF-8):	Dokumentacja API modułu cryptography
Group:		Documentation
BuildArch:	noarch

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

%py3_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst CONTRIBUTING.rst LICENSE LICENSE.APACHE LICENSE.BSD README.rst
%dir %{py3_sitedir}/cryptography
%{py3_sitedir}/cryptography/*.py
%{py3_sitedir}/cryptography/py.typed
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
%dir %{py3_sitedir}/cryptography/hazmat/bindings/_rust
%{py3_sitedir}/cryptography/hazmat/bindings/_rust/*.pyi
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

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_downloads,_static,development,hazmat,x509,*.html,*.js}
%endif
