$(function() {
    
    $.getJSON(api.list(), ({notes}) => $('.note-detail.note-add').before(
        notes.map(renderNoteTemplate).join('')
    ));

    $('body').on('click', '.note-add', function() {
        $.ajax({
            url: api.new(),
            success: showEditPanel,
            error: () => alert('Cannot generate new note!')
        });
    });

    $('#note-list').on('click', '.panel-control #note-update', function() {
        let detail = $(this).parents('.note-detail');
        let slug = detail.data('slug');
        if (!slug) console.error(`Invalid slug: ${detail} ${slug}`);
        else {
            $('#edit-title').val(
                detail.find('.panel-title a:first-child').text()
            );
            $('#edit-text').val(
                detail.find('.panel-text').text()
            );
            showEditPanel(slug);
        }
    }).on('click', '.panel-control #note-delete', function() {
        let slug = $(this).parents('.note-detail').data('slug');
        $.ajax({
            url: api.delete(slug),
            success: () => location.reload(),
            error: () => alert(`Cannot delete Note "${slug}"!`)
        });
    }).on('mouseover', '.panel-title .qricon', function() {
        let qrbox = $(this).siblings('.qrcode');
        if (qrbox.children().length) return;
        let title = $(this).siblings('a[href]');
        qrbox.qrcode({
            render: 'image', size: 1080, radius: 0.5, ecLevel: 'Q',
            mode: 2, label: title.text().slice(0, 4), fontcolor: '#f33',
            mSize: 0.1, mPosX: 0.5, mPosY: 0.5, text: title.prop('href')
        });
    });

    $('#note-edit').on('click', '.panel-edit #save', function() {
        let slug = $('#note-edit').data('slug');
        $.post(api.edit(slug), {
            title: $('#edit-title').val(),
            content: $('#edit-text').val()
        }, (ret) => {
            hideEditPanel();
            location.reload();
        });
    }).on('click', '.panel-edit #cancel', hideEditPanel);

    $('#note-action').on('click', '#note-clear', function() {
        $.get(api.clear(), ()=>location.reload());
    });
});
