<?php session_start();

use Controllers\PdfPseudoAppController;
use Routing\ApplicationRouter;

/**
 * @const application root path
 * @attention ends with /
 */
const APP_ROOT = __DIR__ . "/../";

# init app
require_once(APP_ROOT . "vendor/autoload.php");

# launch app
ApplicationRouter::quickRouting(
    route: $_SERVER["REQUEST_URI"],
    routesMap: [
        "post" => [
            "/pdfpseudo/entities" => [PdfPseudoAppController::class,"provideEntities"],
            "/pdfpseudo/save" => [PdfPseudoAppController::class,"save"]
        ]
    ]
);