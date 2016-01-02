tinymce.init({
    content_style: "body {font-size:14px; margin:0px; padding:0px}",
    selector: "textarea#content",
    theme: "modern",
    plugins: [
        "autoresize advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker",
        "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking",
        "save table contextmenu directionality emoticons template paste textcolor"
    ],
    content_css: "css/content.css",
    toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | l      ink image | print preview media fullpage | forecolor backcolor emoticons",
    style_formats: [{
        title: 'h2二级标题',
        block: 'h2',
        styles: {
            color: '#000'
        }
    }, {
        title: 'h3三级标题',
        block: 'h3',
        styles: {
            color: '#000'
        }
    }, {
        title: 'h4四级标题',
        block: 'h4',
        styles: {
            color: '#000'
        }
    }, {
        title: 'h5五级标题',
        block: 'h5',
        styles: {
            color: '#000'
        }
    }, {
        title: 'h6六级标题',
        block: 'h6',
        styles: {
            color: '#000'
        }
    }, {
        title: 'p标签',
        block: 'p',
        styles: {
            color: '#000'
        }
    }, {
        title: 'Bold text',
        inline: 'b'
    }, {
        title: 'Red text',
        inline: 'span',
        styles: {
            color: '#ff0000'
        }
    }, {
        title: 'Table styles'
    }, {
        title: 'Table row 1',
        selector: 'tr',
        classes: 'tablerow1'
    }],
        language: 'zh_CN'
});

