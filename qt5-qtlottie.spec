#
# Conditional build:
%bcond_without	doc	# Documentation

%define		orgname		qtlottie
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 Lottie (Bodymovin) library
Summary(pl.UTF-8):	Biblioteka Qt5 Lottie (Bodymovin)
Name:		qt5-%{orgname}
Version:	5.15.4
Release:	1
License:	GPL v3+ or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	00974a5be5091eb251b36b0078f0d606
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
BuildRequires:	pkgconfig
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
BuildRequires:	qt5-doc-common >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.016
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Lottie (Bodymovin) library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 Lottie (Bodymovin).

%package -n Qt5Bodymovin
Summary:	The Qt5 Bodymovin library
Summary(pl.UTF-8):	Biblioteka Qt5 Bodymovin
Group:		X11/Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Gui >= %{qtbase_ver}
Requires:	Qt5Qml >= %{qtdeclarative_ver}
Requires:	Qt5Quick >= %{qtdeclarative_ver}

%description -n Qt5Bodymovin
Qt5 Bodymovin library.

%description -n Qt5Bodymovin -l pl.UTF-8
Biblioteka Qt5 Bodymovin.

%package -n Qt5Bodymovin-devel
Summary:	Qt5 Bodymovin - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Bodymovin - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt5Bodymovin = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Gui-devel >= %{qtbase_ver}

%description -n Qt5Bodymovin-devel
Qt5 Bodymovin - development files.

%description -n Qt5Bodymovin-devel -l pl.UTF-8
Biblioteka Qt5 Bodymovin - pliki programistyczne.

%package doc
Summary:	Qt5 Lottie (Bodymovin) documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Lottie (Bodymovin) w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 Lottie (Bodymovin) documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Lottie (Bodymovin) w formacie HTML.

%package doc-qch
Summary:	Qt5 Lottie (Bodymovin) documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Lottie (Bodymovin) w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 Lottie (Bodymovin) documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Lottie (Bodymovin) w formacie QCH.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}

%build
%{qmake_qt5}
%{__make}

%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# drop *.la, rely on qt project files
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Bodymovin -p /sbin/ldconfig
%postun	-n Qt5Bodymovin -p /sbin/ldconfig

%files -n Qt5Bodymovin
%defattr(644,root,root,755)
%doc LICENSE.GPL3-EXCEPT src/unsupported_features.txt
# R: Qt5Core Qt5Gui
%attr(755,root,root) %{_libdir}/libQt5Bodymovin.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Bodymovin.so.5
%dir %{qt5dir}/qml/Qt/labs/lottieqt
# R: Qt5Bodymovin Qt5Core Qt5Gui Qt5Qml Qt5Quick
%attr(755,root,root) %{qt5dir}/qml/Qt/labs/lottieqt/liblottieqtplugin.so
%{qt5dir}/qml/Qt/labs/lottieqt/plugins.qmltypes
%{qt5dir}/qml/Qt/labs/lottieqt/qmldir

%files -n Qt5Bodymovin-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Bodymovin.so
%{_libdir}/libQt5Bodymovin.prl
%{_includedir}/qt5/QtBodymovin
%{_libdir}/cmake/Qt5Bodymovin
%{qt5dir}/mkspecs/modules/qt_lib_bodymovin_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtlottieanimation

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtlottieanimation.qch
%endif
