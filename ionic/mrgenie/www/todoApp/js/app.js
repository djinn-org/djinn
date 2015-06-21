angular.module('todoApp', ['ionic', 'todoApp.controllers', 'todoApp.services'])
    .run(function ($ionicPlatform) {
        $ionicPlatform.ready(function () {
            // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
            // for form inputs)
            if (window.cordova && window.cordova.plugins && window.cordova.plugins.Keyboard) {
                cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
            }
            if (window.StatusBar) {
                // org.apache.cordova.statusbar required
                StatusBar.styleLightContent();
            }
            //$state.go('todos');
        });
    })
    .config(function ($stateProvider) {
        $stateProvider
        .state('todos', {
            url: '/todos',
            views: {
                todos: {
                    controller: 'TodoListController',
                    templateUrl: 'views/todos.html'
                }
            }
        })
        .state('createTodo', {
            url: '/todo/new',
            controller: 'TodoCreationController',
            templateUrl: 'views/create-todo.html'
        })
        .state('settings', {
            url: '/todo/settings',
            controller: 'AccountCtrl',
            templateUrl: 'templates/tab-account.html'
        })
        .state('settings2', {
            url: '/todo/settings2',
            views: {
                todos: {
                    controller: 'AccountCtrl',
                    templateUrl: 'templates/tab-account.html'
                }
            }
        })
        .state('editTodo', {
            url: '/todo/edit/:id/:content',
            controller: 'TodoEditController',
            templateUrl: 'views/edit-todo.html'
        });

        // if none of the above states are matched, use this as the fallback
        $urlRouterProvider.otherwise('/todo/new');

    });
