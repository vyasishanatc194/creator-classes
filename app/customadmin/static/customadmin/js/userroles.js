/*global $ */
'use strict';

var userroles = {

    // ------------------------------------------------------------------------
    // Users
    // ------------------------------------------------------------------------
    users: {
        index: function () {
            $('#user-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },],
            });
        },
        details: function () {
            $('.groups-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available groups',
                selectedListLabel: 'Chosen groups',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }
    },
    // ------------------------------------------------------------------------
    // User Card
    // ------------------------------------------------------------------------
    usercards: {
        index: function () {
            $('#usercard-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },

        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }

    },
    // ------------------------------------------------------------------------
    // Creators
    // ------------------------------------------------------------------------
    creators: {

        index: function () {
            $('#creator-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },

        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }

    },
    // ------------------------------------------------------------------------
    // Admin Keywords
    // ------------------------------------------------------------------------
    adminkeywords: {

        index: function () {
            $('#adminkeyword-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },

        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }

    },
    // ------------------------------------------------------------------------
    // Testimonials
    // ------------------------------------------------------------------------
    testimonials: {

        index: function () {
            $('#testimonial-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },

        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }

    },
    // ------------------------------------------------------------------------
    // CreatorClasses
    // ------------------------------------------------------------------------
    creatorclasses: {

        index: function () {
            $('#creatorclass-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },

        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }

    },
    // ------------------------------------------------------------------------
    // streams
    // ------------------------------------------------------------------------
    streams: {

        index: function () {
            $('#stream-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },

        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }

    },
    // ------------------------------------------------------------------------
    // stream booking
    // ------------------------------------------------------------------------
    streambookings: {

        index: function () {
            $('#streambooking-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },

        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }

    },
    // ------------------------------------------------------------------------
    // session booking
    // ------------------------------------------------------------------------
    sessionbookings: {

        index: function () {
            $('#sessionbooking-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },

        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }

    },
    // ------------------------------------------------------------------------
    // ClassReviews
    // ------------------------------------------------------------------------
    classreviews: {

        index: function () {
            $('#classreview-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },

        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }

    },
    // ------------------------------------------------------------------------
    // ClassReviews
    // ------------------------------------------------------------------------
    onetoonesessions: {

        index: function () {
            $('#onetoonesession-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },

        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }

    },
    // ------------------------------------------------------------------------
    // CreatorReviews
    // ------------------------------------------------------------------------
    creatorreviews: {

        index: function () {
            $('#creatorreview-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },

        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }

    },
    // ------------------------------------------------------------------------
    // Material
    // ------------------------------------------------------------------------
    materials: {

        index: function () {
            $('#material-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },

        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }

    },
    // ------------------------------------------------------------------------
    // ------------------------------------------------------------------------
    // MaterialCategory
    // ------------------------------------------------------------------------
    materialcategories: {

        index: function () {
            $('#materialcategory-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },

        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }

    },
    // ------------------------------------------------------------------------
    // Plan
    // ------------------------------------------------------------------------
    plans: {

        index: function () {
            $('#plan-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },

        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }

    },
    // ------------------------------------------------------------------------
    // Groups
    // ------------------------------------------------------------------------
    groups: {

        index: function () {
            $('#group-table').DataTable({
                order: [],
                pageLength: 25,
                responsive: true,
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },

        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }

    },


};
