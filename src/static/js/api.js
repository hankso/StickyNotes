// We should avoid using HTTP method PUT & DELETE 
// because it may not be supported by all browsers.
const api = {
    view:   (slug) => `note/${slug}`,
    edit:   (slug) => `note/${slug}`,
    delete: (slug) => `clear?slug=${slug}`,
    new:    ()     => 'new',
    list:   ()     => 'list',
    clear:  (slug) => slug ? `clear?slug=${slug}` : 'clear',
};
