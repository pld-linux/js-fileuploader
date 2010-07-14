Summary:	AJAX Upload
Name:		js-ajax-upload
Version:	3.9
Release:	1
License:	MIT
Group:		Applications/WWW
Source0:	http://download.github.com/valums-ajax-upload-%{version}-0-g6f977de.zip
# Source0-md5:	89d8611a5f6a51230486acab2cb46722
URL:		http://valums.com/ajax-upload/
BuildRequires:	js
BuildRequires:	unzip
BuildRequires:	yuicompressor
Requires:	webserver(access)
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
AJAX Upload allows you to easily upload multiple files without
refreshing the page and use any element to show file selection window.
It works in all major browsers and doesn’t require any library to run.
AJAX Upload doesn’t pollute the global namespace, and is tested with
jQuery, Prototypejs.

%package demo
Summary:	Demo for AJAX Upload
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu AJAX Upload
Group:		Development
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for AJAX Upload.

%prep
%setup -qc
mv valums-ajax-upload-*/* .

mv readme.md README

# Apache1/Apache2 config
cat > apache.conf <<'EOF'
Alias /js/ajax-upload %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

# lighttpd config
cat > lighttpd.conf <<'EOF'
alias.url += (
	"/js/ajax-upload" => "%{_appdir}",
)
EOF

%build
install -d build
for a in *.js; do
	yuicompressor --charset UTF-8 $a > build/$a
	js -C -f build/$a
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_examplesdir}/%{name}-%{version}}
cp -a build/ajaxupload.js $RPM_BUILD_ROOT%{_appdir}

cp -a demos server-side tests $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%{_appdir}

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
