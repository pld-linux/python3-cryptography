#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit test

%define		crates_ver	35.0.0

Summary:	Crypthography library for Python 3
Summary(pl.UTF-8):	Biblioteka Cryptography dla Pythona 3
Name:		python3-cryptography
Version:	35.0.0
Release:	2
License:	Apache v2.0 or BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cryptography/
Source0:	https://files.pythonhosted.org/packages/source/c/cryptography/cryptography-%{version}.tar.gz
# Source0-md5:	ba34eba3ae36cbf3d2e1ee3239f07732
#Source1Download: https://pypi.org/simple/cryptography_vectors/
Source1:	https://files.pythonhosted.org/packages/source/c/cryptography-vectors/cryptography_vectors-%{version}.tar.gz
# Source1-md5:	8e9d050bd601d1788883fa361c69cf85
# cd cryptography-%{version}/src/rust
# cargo vendor
# tar cJf python3-cryptography-crates-%{version}.tar.xz vendor Cargo.lock
Source2:	%{name}-crates-%{crates_ver}.tar.xz
# Source2-md5:	c3398eb08b99552f09b8b8f16d0d3910
URL:		https://cryptography.io/
BuildRequires:	openssl-devel >= 1.1.0
BuildRequires:	python3-cffi >= 1.12
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-setuptools >= 1:18.5
BuildRequires:	python3-setuptools_rust
BuildRequires:	python3-six >= 1.4.1
BuildRequires:	rpm-pythonprov >= 5.4.15-48
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	rust >= 1.41.0
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
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%endif
Requires:	openssl >= 1.1.0
ExclusiveArch:	%{rust_arches}
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

cd src/rust
tar xf %{SOURCE2}
# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/src/rust/.cargo"
export CARGO_OFFLINE=true
export RUSTFLAGS="%{rpmrustflags}"
export CARGO_TERM_VERBOSE=true
%ifarch x32
export CARGO_BUILD_TARGET=x86_64-unknown-linux-gnux32
%endif

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

export CARGO_HOME="$(pwd)/src/rust/.cargo"
export CARGO_OFFLINE=true
export RUSTFLAGS="%{rpmrustflags}"
export CARGO_TERM_VERBOSE=true
%ifarch x32
export CARGO_BUILD_TARGET=x86_64-unknown-linux-gnux32
%endif

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
