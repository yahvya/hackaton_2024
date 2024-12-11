<?php

// routes web

use Controllers\TestController;
use SaboCore\Routing\Routes\Route;
use SaboCore\Routing\Routes\RouteManager;

RouteManager::registerRoute(
    Route::post(
        link: "/juroshpdfmerge",
        toExecute: [TestController::class,"juroshpdfmerge"],
        routeName: "sabo"
    )
);
