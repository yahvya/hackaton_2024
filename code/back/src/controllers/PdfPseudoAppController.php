<?php

namespace Controllers;

use PdfPseudoApp\App\PdfPseudoApp;
use PdfPseudoApp\Utils\DefaultLogger;
use Routing\ApplicationRouter;
use Throwable;

/**
 * @brief pdf app treatment controller
 */
class PdfPseudoAppController extends AbstractController {
    /**
     * @brief provide the entities to mask for the provided pdf
     * @return never
     */
    public function provideEntities():never{
        $this->renderJson([
            ["pdfAsBlob" => base64_encode(file_get_contents("C:\Users\Etudiant\Desktop\\fichiers-temporaires\\facture.pdf"))],
            ["pdfAsBlob" => base64_encode(file_get_contents("C:\Users\Etudiant\Desktop\\fichiers-temporaires\\BACHIRCV.pdf"))]
        ]);
        if(!array_key_exists(key: "pdfs",array: $_FILES))
            ApplicationRouter::unauthorized(["error" => "Please provide a pdf file"]);

        # init logger
        $logger = new DefaultLogger(logFileAbsolutePath: APP_ROOT . "private-storage/log.txt");

        # convert to normalized arrays
        $normalizedDatas = [];

        foreach($_FILES["pdfs"]["tmp_name"] as $index => $tmpName) {
            $normalizedDatas[] = [
                "tmp_name" => $tmpName,
                "name" => $_FILES["pdfs"]["name"][$index],
                "type" => $_FILES["pdfs"]["type"][$index],
                "size" => $_FILES["pdfs"]["size"][$index],
                "error" => $_FILES["pdfs"]["error"][$index]
            ];
        }

        # check the provided file security
        if(!PdfPseudoApp::isUploadedFileSecure(fileDatas: $normalizedDatas,logger: $logger))
            ApplicationRouter::unauthorized(message: ["error" => "Please send a valid pdf file"]);

        $pdfPseudoApp = new PdfPseudoApp(
            pdfFilePaths: array_map(fn(array $datas):string => $datas["tmp_name"],$normalizedDatas),
            pythonScriptPath: APP_ROOT . "data-extraction/app.py",
            privateStoragePath: APP_ROOT . "private-storage/",
            logger: $logger
        );

        try{
            $this->renderJson(json: $pdfPseudoApp->getEntitiesToTransform());
        }
        catch(Throwable){
            ApplicationRouter::internalError();
        }
    }
}