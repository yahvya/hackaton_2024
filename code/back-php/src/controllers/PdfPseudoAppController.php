<?php

namespace Controllers;

use PdfPseudoApp\App\PdfPseudoApp;
use PdfPseudoApp\Utils\DefaultLogger;
use Routing\ApplicationRouter;

/**
 * @brief pdf app treatment controller
 */
class PdfPseudoAppController extends AbstractController {
    public function index():void{
        if(!array_key_exists(key: "pdf",array: $_FILES))
            ApplicationRouter::unauthorized(["error" => "Please provide a pdf file"]);

        # init logger
        $logger = new DefaultLogger(logFileAbsolutePath: APP_ROOT . "private-storage/log.txt");

        # check the provided file security
        if(!PdfPseudoApp::isUploadedFileSecure(fileData: $_FILES["pdf"],logger: $logger))
            ApplicationRouter::unauthorized(message: ["error" => "Please send a valid pdf file"]);

        $pdfPseudoApp = new PdfPseudoApp(pdfFilePath: $_FILES["pdf"]["tmp_name"],logger: $logger);
        $pdfPseudoApp->getEntitiesToTransform();

        die("ici");
    }
}