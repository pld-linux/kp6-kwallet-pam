#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.1.4
%define		qtver		5.15.2
%define		kpname		kwallet-pam
Summary:	KWallet PAM integration
Name:		kp6-%{kpname}
Version:	6.1.4
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		Base
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	801318aea037e3d64f0aa7c9ca4fef8b
URL:		http://www.kde.org/
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf6-extra-cmake-modules >= 1.4.0
BuildRequires:	pam-devel
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	kp5-%{kpname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KWallet PAM integration.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DCMAKE_INSTALL_LIBDIR:PATH=/%{_lib} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_kwallet5.so
/etc/xdg/autostart/pam_kwallet_init.desktop
%attr(755,root,root) %{_libexecdir}/pam_kwallet_init
%{systemduserunitdir}/plasma-kwallet-pam.service
