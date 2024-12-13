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

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept');

# launch app
ApplicationRouter::quickRouting(
    route: $_SERVER["REQUEST_URI"],
    routesMap: [
        "post" => [
            "/pdfpseudo/entities" => [PdfPseudoAppController::class,"provideEntities"],
            "/pdfpseudo/reload" => [PdfPseudoAppController::class,"reload"],
            "/pdfpseudo/status" => [PdfPseudoAppController::class,"status"],
        ]
    ]
);