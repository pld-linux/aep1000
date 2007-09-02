Summary:	Utilities for AEP1000 SSL Accelerator
Summary(pl.UTF-8):	Narzędzia dla akceleratora AEP1000 SSL Accelerator
Name:		aep1000
Version:	2.1
Release:	1
License:	BSD
Group:		Applications/System
Source0:	aep_host_sw.tar.gz
# Source0-md5:	7a34b93e9dbeadad28b4a8c2a522b992
Source1:	aeptarg.bin
# Source1-md5:	dc6e1cadea20006fc9e3f457b23d32c5
Patch0:		%{name}-redhat.patch
Patch1:		%{name}-make.patch
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utilities for AEP1000 SSL Accelerator.

%description -l pl.UTF-8
Narzędzia dla akceleratora AEP1000 SSL Accelerator.

%package libs
Summary:	AEP SSL Accelerator SDK library
Summary(pl.UTF-8):	Biblioteka SDK akceleratora AEP SSL Accelerator
Group:		Libraries

%description libs
AEP SSL Accelerator SDK library.

%description libs -l pl.UTF-8
Biblioteka SDK akceleratora AEP SSL Accelerator.

%package devel
Summary:	Header files for AEP library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki AEP
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for AEP library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki AEP.

%package static
Summary:	Static AEP library
Summary(pl.UTF-8):	Statyczna biblioteka AEP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static AEP library.

%description static -l pl.UTF-8
Statyczna biblioteka AEP.

%prep
%setup -q -c
%patch0 -p0
%patch1 -p0

%build
cd Host
ln -s libaep.so.1 API/libaep.so
%{__make} -C API \
	CC="%{__cc}" \
	LD="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcflags}"
cd API
ar rcs libaep.a *.o
cd ..
%{__make} -C Daemon \
	CC="%{__cc}" \
	LD="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcflags}"
%{__make} -C Test/quicktest \
	CC="%{__cc}" \
	LD="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcflags}"
%{__make} -C versionApp \
	CC="%{__cc}" \
	LD="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcflags}"
%{__make} -C aeploader \
	CC="%{__cc}" \
	LD="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -D Host/API/libaep.so.1 $RPM_BUILD_ROOT%{_libdir}/libaep.so.1
ln -sf libaep.so.1 $RPM_BUILD_ROOT%{_libdir}/libaep.so
install Host/API/libaep.a $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_includedir}
install Host/h/*.h $RPM_BUILD_ROOT%{_includedir}

install -D Host/Daemon/aepdaemon $RPM_BUILD_ROOT%{_sbindir}/aepdaemon
install Host/Test/quicktest/aeptest $RPM_BUILD_ROOT%{_sbindir}
install Host/aeploader/aepload $RPM_BUILD_ROOT%{_sbindir}
install Host/versionApp/aepversion $RPM_BUILD_ROOT%{_sbindir}

install -D %{SOURCE1} $RPM_BUILD_ROOT/lib/firmware/aeptarg.bin

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/aepdaemon
%attr(755,root,root) %{_sbindir}/aepload
%attr(755,root,root) %{_sbindir}/aeptest
%attr(755,root,root) %{_sbindir}/aepversion
/lib/firmware/aeptarg.bin

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaep.so.*
# dlopened by openssl engine
%attr(755,root,root) %{_libdir}/libaep.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/aep_*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libaep.a
