#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit test

%define		crates_ver	45.0.4

Summary:	Crypthography library for Python 3
Summary(pl.UTF-8):	Biblioteka Cryptography dla Pythona 3
Name:		python3-cryptography
Version:	45.0.4
Release:	1
License:	Apache v2.0 or BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cryptography/
Source0:	https://files.pythonhosted.org/packages/source/c/cryptography/cryptography-%{version}.tar.gz
# Source0-md5:	6d8a9d089f9c434c200e51d53cfa2ea5
#Source1Download: https://pypi.org/simple/cryptography_vectors/
Source1:	https://files.pythonhosted.org/packages/source/c/cryptography-vectors/cryptography_vectors-%{version}.tar.gz
# Source1-md5:	76f9e68acd6adbfdea3648cc77284e72
# cd cryptography-%{version}/src/rust
# cargo vendor
# tar cJf python3-cryptography-crates-%{version}.tar.xz vendor Cargo.lock
Source2:	%{name}-crates-%{crates_ver}.tar.xz
# Source2-md5:	0b6a97842d4a807a250ab556c67889a1
URL:		https://cryptography.io/
BuildRequires:	openssl-devel >= 1.1.1d
BuildRequires:	python3-build >= 1.0.0
BuildRequires:	python3-cffi >= 1.14
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-installer
BuildRequires:	python3-maturin >= 1.8.6
BuildRequires:	python3-maturin < 2
BuildRequires:	python3-setuptools >= 1:75
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov >= 5.4.15-48
BuildRequires:	rpmbuild(macros) >= 2.044
BuildRequires:	rust >= 1.56.0
%if %{with tests}
BuildRequires:	python3-certifi >= 2024
BuildRequires:	python3-pretend >= 0.7
BuildRequires:	python3-pytest >= 7.4.0
BuildRequires:	python3-pytest-benchmark >= 4.0
BuildRequires:	unzip
%endif
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme >= 3.0.0
BuildRequires:	python3-sphinx_inline_tabs
BuildRequires:	sphinx-pdg-3 >= 5.3.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%endif
Requires:	openssl >= 1.1.1d
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
cat >.cargo/config.toml <<EOF
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
export PKG_CONFIG_ALLOW_CROSS=1
export PYO3_CROSS_LIB_DIR=%{_libdir}
%endif

export CFLAGS="%{rpmcflags}"

%py3_build_pyproject

%if %{with tests} || %{with doc}
%{__unzip} -qo build-3/*.whl -d build-3/test-path
%endif

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_benchmark.plugin" \
PYTHONPATH=$(pwd)/build-3/test-path \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/build-3/test-path \
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
export PKG_CONFIG_ALLOW_CROSS=1
%endif

%py3_install_pyproject

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
%dir %{py3_sitedir}/cryptography/hazmat/bindings/_rust/openssl
%{py3_sitedir}/cryptography/hazmat/bindings/_rust/openssl/*.pyi
%dir %{py3_sitedir}/cryptography/hazmat/bindings/openssl
%{py3_sitedir}/cryptography/hazmat/bindings/openssl/*.py
%{py3_sitedir}/cryptography/hazmat/bindings/openssl/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/decrepit
%{py3_sitedir}/cryptography/hazmat/decrepit/*.py
%{py3_sitedir}/cryptography/hazmat/decrepit/__pycache__
%dir %{py3_sitedir}/cryptography/hazmat/decrepit/ciphers
%{py3_sitedir}/cryptography/hazmat/decrepit/ciphers/*.py
%{py3_sitedir}/cryptography/hazmat/decrepit/ciphers/__pycache__
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
%{py3_sitedir}/cryptography-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_downloads,_static,development,hazmat,x509,*.html,*.js}
%endif
