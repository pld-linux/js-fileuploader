%define		plugin	fileuploader
Summary:	Multiple file upload plugin with progress-bar, drag-and-drop
Name:		js-%{plugin}
Version:	2.0
Release:	2
License:	MIT, GPL v2 or LGPL v2
Group:		Applications/WWW
Source0:	https://github.com/downloads/valums/file-uploader/%{version}.zip
# Source0-md5:	0b45522b5337b38e1720dc9600337b5d
URL:		https://github.com/valums/file-uploader
BuildRequires:	closure-compiler
BuildRequires:	js
BuildRequires:	unzip
BuildRequires:	yuicompressor
Requires:	webserver(access)
Requires:	webserver(alias)
#Obsoletes:	js-ajax-upload
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
This project attempts to achieve a user-friendly file-uploading
experience over the web. It's built as a Javascript plugin for
developers looking to incorporate file-uploading into their website.

This plugin uses an XMLHttpRequest (AJAX) for uploading multiple files
with a progress-bar in FF3.6+, Safari4+, Chrome and falls back to
hidden-iframe-based upload in other browsers (namely IE), providing
good user experience everywhere.

It does not use Flash, jQuery, or any external libraries.

%package demo
Summary:	Demo for %{plugin}
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu %{plugin}
Group:		Development
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for %{plugin}.

%prep
%setup -qc

# Apache1/Apache2 config
cat > apache.conf <<'EOF'
Alias /js/%{plugin} %{_appdir}
<Directory %{_appdir}>
	Allow from all
	Options +FollowSymLinks
</Directory>
EOF

# lighttpd config
cat > lighttpd.conf <<'EOF'
alias.url += (
	"/js/%{plugin}" => "%{_appdir}",
)
EOF

%build
install -d build

# pack .css
for css in *.css; do
	out=build/${css#*/}
%if 0%{!?debug:1}
	yuicompressor --charset UTF-8 $css -o $out
%else
	cp -p $css $out
%endif
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_examplesdir}/%{name}-%{version}}
cp -p %{plugin}.min.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.min.js
cp -p %{plugin}.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.js
ln -s %{plugin}-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}.js

cp -p %{plugin}.css $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.css
cp -p build/%{plugin}.css $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.min.css
ln -s %{plugin}-%{version}.min.css $RPM_BUILD_ROOT%{_appdir}/%{plugin}.css

cp -p loading.gif  $RPM_BUILD_ROOT%{_appdir}

cp -a *.htm $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -p apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

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
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%{_appdir}

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
